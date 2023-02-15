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
use Word;

package CoordinatingConjunction;

sub get_cc_parts($graph, $word) {
    my @cc_parts;
    my $id = Word::id($word);
    for my $conj_id (Graph::get_radj_ids_if($graph, $id, \&Word::is_conj)) {
        my @ccs = Graph::get_radj_ids_if($graph, $conj_id, \&Word::is_cc);
        push @cc_parts, ($conj_id, @ccs) if @ccs;
    }
    return @cc_parts;
}

1;
