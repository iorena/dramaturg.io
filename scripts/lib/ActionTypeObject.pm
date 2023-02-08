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

    my $word = $matching_words[0];
    my $id = Word::id($word);

    # Get any nummods and/or determiners.
    my @nummods = Graph::get_radj_ids_if($graph, $id, \&Word::is_nummod);
    my @determiners = Graph::get_radj_ids_if($graph, $id, \&Word::is_det);

    $action_type->{'object'} = join(' ', (map { Word::lemma(Graph::get_word($graph, $_)) } Utils::intsort (@nummods, @determiners, $id)));
    $action_type->{'object_case'} = Word::get_feat($word, "Case");
    $action_type->{'object_number'} = Word::get_feat($word, "Number");

    return 1;
}

1;
