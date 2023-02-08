#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

use Graph;
use Utils;
use Word;

package ActionTypeObject;

sub process_object($action_type, $graph, $verb_id) {
    my @matching_words = Graph::get_radj_if($graph, $verb_id, \&Word::is_obj);

    unless (@matching_words > 0) {
        Output::log_msg("    Continue: no object word found.\n");
        return 0;
    }

    unless (@matching_words == 1) {
        Output::log_msg("    Continue: multiple object words found.\n");
        return 0;
    }

    my $object_word = $matching_words[0];
    my $object_id = Word::id($object_word);

    # Get any nummods and/or determiners.
    my @nummods = Graph::get_radj_ids_if($graph, $object_id, \&Word::is_nummod);
    my @determiners = Graph::get_radj_ids_if($graph, $object_id, \&Word::is_det);

    if (@nummods || @determiners) {
        $action_type->{'object'} = join(' ', (map { Word::form(Graph::get_word($graph, $_)) } Utils::intsort (@nummods, @determiners, $object_id)));
    } else {
        $action_type->{'object'} = Word::lemma($object_word);
        $action_type->{'object_case'} = Word::get_feat($object_word, "Case");
        $action_type->{'object_number'} = Word::get_feat($object_word, "Number");
    }

    return 1;
}

1;
