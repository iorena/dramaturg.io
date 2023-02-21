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
    for my $conj (Graph::get_radj_if($graph, Word::id($word), \&Word::is_conj)) {
        my @ccs = Graph::get_radj_if($graph, Word::id($conj), \&Word::is_cc);
        push @cc_parts, ($conj, @ccs) if @ccs;
    }
    return sort { Word::id($a) <=> Word::id($b) } @cc_parts;
}

sub get_cc_parts_as_ids($graph, $word) { return map { Word::id($_) } get_cc_parts($graph, $word); }

1;
