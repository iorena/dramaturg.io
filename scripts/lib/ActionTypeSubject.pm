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
use Utils;
use Word;

package ActionTypeSubject;

sub get_person($graph, $verb_id) {
    my $person = Word::get_feat(Graph::get_word($graph, $verb_id), "Person");
    
    if (!$person) {
        # Check auxiliary verbs.
        for (Graph::get_radj_if($graph, $verb_id, \&Word::is_aux)) {
            $person = Word::get_feat($_, "Person") if !$person;
        }
    }

    return $person;
}

sub process_subject($action_type, $graph, $verb_id) {
    my @matching_words = Graph::get_radj_if($graph, $verb_id, \&Word::is_nsubj);

    if (@matching_words == 0) {
        # Attempt to set (implicit) subject through the verb's "Person" feat.
        my $person = get_person($graph, $verb_id);

        unless ($person && $person ne "3") {
            Output::log_msg("    Continue: no subject word found.\n");
            return 0;
        }

        $action_type->{'subject'} = Convert::person($person);

        return 1;
    }

    unless (@matching_words == 1) {
        Output::log_msg("    Continue: multiple subject words found.\n");
        return 0;
    }

    my $word = $matching_words[0];
    my $id = Word::id($word);

    # Get any flat:names and/or determiners.
    my @flatnames = Graph::get_radj_ids_if($graph, $id, \&Word::is_flat);
    my @determiners = Graph::get_radj_ids_if($graph, $id, \&Word::is_det);
        
    $action_type->{'subject'} = join(' ', (map { Word::form(Graph::get_word($graph, $_)) } Utils::intsort (@flatnames, @determiners, $id)));

    return 1;
}

1;
