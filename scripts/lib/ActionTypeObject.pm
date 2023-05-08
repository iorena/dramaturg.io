#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

use Convert;
use Conjunction;
use Graph;
use Log;
use Person;
use Utils;
use Word;

package ActionTypeObject;

sub process_object($action_type, $graph, $verb_id) {
    my @matching_words = Graph::get_radj_if($graph, $verb_id, \&Word::is_obj);

    unless (@matching_words > 0) {
        Log::write_out_indented("Continue: no object word found.\n");
        return 0;
    }

    unless (@matching_words == 1) {
        Log::write_out_indented("Continue: multiple object words found: " . Utils::list_word_forms_quoted(@matching_words) . ".\n");
        return 0;
    }

    my $object_word = $matching_words[0];
    my $object_id = Word::id($object_word);

    if (Word::is_verb($object_word)) {
        Log::write_out_indented("Continue: skip verb objects. \"" . Word::form($object_word) . "\".\n");
        return 0;
    }

    if (Word::is_intj($object_word)) {
        Log::write_out_indented("Continue: skip interjection objects: \"" . Word::form($object_word) . "\".\n");
        return 0;
    }

    my @ces = Conjunction::get_coordinated_elements($graph, $object_word);
    if (@ces) {
        Log::write_out_indented("Continue: coordinated elements in object: \"" . Word::form($object_word) . "\" -> " . Utils::list_word_forms_quoted(@ces) . ".\n");
        return 0;
    }

    my @adps = Graph::get_radj_if($graph, $object_id, \&Word::is_adp);
    if (@adps) {
        Log::write_out_indented("Continue: adpositional relation in object: \"" . Word::form($object_word) . "\" -> " . Utils::list_word_forms_quoted(@adps) . ".\n");
        return 0;
    }

    # Analyze neighboring words in sentence.
    for my $next_id ($object_id - 1, $object_id + 1) {
        my $order = $next_id == $object_id - 1 ? "previous" : "next";
        if (Graph::contains($graph, $next_id)) {
            my $next_word = Graph::get_word($graph, $next_id);
            my $is_obl = Word::is_obl($next_word);
            my $is_nmod = Word::is_nmod($next_word);
            if ($is_obl || $is_nmod) {
                my $reason = $is_obl ? "oblique nominal" : "nominal modifier";
                Log::write_out_indented("Continue: skip not sufficiently stand-alone object word: \"" . Word::form($object_word) . "\" -> $order $reason word \"" . Word::form($next_word) . "\".\n");
                return 0;
            }
        }
    }

    # Get any nummods and/or determiners.
    my @nummods = Graph::get_radj_ids_if($graph, $object_id, \&Word::is_nummod);
    my @determiners = Graph::get_radj_ids_if($graph, $object_id, \&Word::is_det);

    if (@nummods || @determiners) {
        # Multi-word object with nummods and determiners attached.
        $action_type->{'object'} = join(" ", (map { Person::form_or_person_if(Graph::get_word($graph, $_), \&Word::is_obj) } Utils::intsort (@nummods, @determiners, $object_id)));
    } else {
        # Single-word object.
        my ($case, $number) = Word::get_feats($object_word, ("Case", "Number"));

        unless ($case && $number) {
            Log::write_out_indented("Continue: object word missing 'Case' and 'Number' feats: \"" . Word::form($object_word) . "\".\n");
            return 0;
        }

        $action_type->{'object'} =  Person::lemma_or_person_if($object_word, \&Word::is_obj);
        $action_type->{'object_case'} = Convert::case($case);
        $action_type->{'object_number'} = Convert::number($number);
    }

    # Mark object as proper noun with private key in case word will be generalized later.
    $action_type->{'object_is_propn'} = 1 if Word::is_propn($object_word);

    # Save object id with private key 'object_id'.
    $action_type->{'object_id'} = $object_id;

    return 1;
}

1;
