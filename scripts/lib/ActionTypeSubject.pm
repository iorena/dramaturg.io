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

package ActionTypeSubject;

sub process_subject($action_type, $graph, $verb_id) {
    my @matching_words = Graph::get_radj_if($graph, $verb_id, \&Word::is_nsubj);

    if (@matching_words == 0) {
        # Attempt to set (implicit) subject through the verb's "Person" feat.
        my $person = Person::get_implicit_person_from_verb($graph, $verb_id);

        unless (Person::valid_person($person)) {
            Log::write_out_indented("Continue: no subject word found.\n");
            return 0;
        }

        $action_type->{'subject'} = Convert::person($person);

        # Save subject id (the verb id in this case) with private key 'subject_id'.
        $action_type->{'subject_id'} = $verb_id;

        return 1;
    }

    unless (@matching_words == 1) {
        Log::write_out_indented("Continue: multiple subject words found: " . Utils::quoted_word_forms(@matching_words) . ".\n");
        return 0;
    }

    my $subject_word = $matching_words[0];

    my @ces = Conjunction::get_coordinated_elements($graph, $subject_word);
    if (@ces) {
        Log::write_out_indented("Continue: coordinated elements in subject: \"" . Word::form($subject_word) . "\" -> " . Utils::quoted_word_forms(@ces) . ".\n");
        return 0;
    }

    my $subject_id = Word::id($subject_word);

    # Mark subject as proper noun with private key in case word will be generalized later.
    $action_type->{'subject_is_propn'} = 1 if Word::is_propn($matching_words[0]);

    # Get any flat:names and/or determiners.
    my @flatnames = Graph::get_radj_ids_if($graph, $subject_id, \&Word::is_flat);
    my @determiners = Graph::get_radj_ids_if($graph, $subject_id, \&Word::is_det);
        
    $action_type->{'subject'} = join(" ", (map { Person::form_or_person_if(Graph::get_word($graph, $_), \&Word::is_nsubj) } Utils::intsort (@flatnames, @determiners, $subject_id)));

    # Save subject id with private key 'subject_id'.
    $action_type->{'subject_id'} = $verb_id;

    return 1;
}

1;
