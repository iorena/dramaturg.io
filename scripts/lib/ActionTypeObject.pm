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
use Graph;
use Log;
use Person;
use Utils;
use Word;

package ActionTypeObject;

sub process_object($action_type, $graph, $verb_id) {
    my @matching_words = Graph::get_radj_if($graph, $verb_id, \&Word::is_obj);

    unless (@matching_words > 0) {
        Log::message("    Continue: no object word found.\n");
        return 0;
    }

    unless (@matching_words == 1) {
        Log::message("    Continue: multiple object words found.\n");
        return 0;
    }

    my $object_word = $matching_words[0];

    if (Word::is_intj($object_word)) {
        Log::message("    Continue: skip interjection objects.\n");
        return 0;
    }

    my $object_id = Word::id($object_word);

    # Mark object as proper noun with private key in case word will be generalized later.
    $action_type->{'object_is_propn'} = 1 if Word::is_propn($object_word);


    # Get any nummods and/or determiners.
    my @nummods = Graph::get_radj_ids_if($graph, $object_id, \&Word::is_nummod);
    my @determiners = Graph::get_radj_ids_if($graph, $object_id, \&Word::is_det);

    if (@nummods || @determiners) {
        $action_type->{'object'} = join(" ", (map { Person::form_or_person_if(Graph::get_word($graph, $_), \&Word::is_obj) } Utils::intsort (@nummods, @determiners, $object_id)));
    } else {
        $action_type->{'object'} =  Person::lemma_or_person_if($object_word, \&Word::is_obj);
        $action_type->{'object_case'} = Convert::case(Word::get_feat($object_word, "Case"));
        $action_type->{'object_number'} = Convert::number(Word::get_feat($object_word, "Number"));
    }

    return 1;
}

1;
