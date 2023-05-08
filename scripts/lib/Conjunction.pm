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

package Conjunction;

# In addition to implicit conjuncts ("conj"), return true also for the word at root and parataxis words.
sub is_conjunction_word($graph, $word) { return Word::is_root($word) || Word::is_conj($word) || Word::is_parataxis($word); }

sub get_coordinated_conjunctions($graph, $word) { return Graph::get_radj_if($graph, Word::id($word), \&Word::is_cc); }

# Get conjunct elements connected by a coordinating conjunction (cc) and get those as well.
sub get_coordinated_elements($graph, $word) { 
    my @coordinated_elements;
    for my $conj (Graph::get_radj_if($graph, Word::id($word), \&Word::is_conj)) {
        my @ccs = get_coordinated_conjunctions($graph, $conj);
        push @coordinated_elements, ($conj, @ccs) if @ccs;
    }
    return sort { Word::id($a) <=> Word::id($b) } @coordinated_elements;
}

sub get_coordinated_elements_as_ids($graph, $word) { return map { Word::id($_) } get_coordinated_elements($graph, $word); }

1;
