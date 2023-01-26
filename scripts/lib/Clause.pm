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

package Clause;

# Root/conjunction/parataxis words start new clauses.
sub starts_new_clause($word) { return Word::is_root($word) || Word::is_conj($word) || Word::is_parataxis($word); }

# Find clauses by running a recursive search through the reverse dependency graph.
sub find_clauses($graph, $graph_clauses, $node, $i) {
    for (Graph::get_radj($graph, $i)) {
        my $id = Word::id($_);
        if (starts_new_clause($_)) {
            $graph_clauses->{$id} = [$id];
            find_clauses($graph, $graph_clauses, $id, $id);
        } else {
            push $graph_clauses->{$node}->@*, $id;
            find_clauses($graph, $graph_clauses, $node, $id);
        }
    }
}

# Infers clauses in a sentence through the dependency graph.
sub get_clauses($graph) {
    my $root = Graph::get_root_id($graph);
    my %graph_clauses = ( $root => [$root] );
    find_clauses($graph, \%graph_clauses, $root, $root);
    return %graph_clauses;
}

1;
