#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

use Conjunction;
use Utils;
use Word;

package ClauseGraph;

sub clause_node($word_id, $parent_id) {
    return {
        'word_id' => $word_id,
        'parent_id' => $parent_id,
        'word_ids' => [$word_id],
        'adj' => []
    };
}

# Create and connect clause nodes with a recursive DFS through the dependency graph.
sub connect_conjunctions($graph, $clause_graph, $clause_node_id, $id) {
    for my $next_id (Graph::get_radj_ids($graph, $id)) {
        if (Conjunction::is_conjunction_word($graph, Graph::get_word($graph, $next_id))) {
            # Word is conjunction: create new clause node.
            $clause_graph->{$next_id} = clause_node($next_id, $clause_node_id);

            # Connect new clause node to parent.
            push $clause_graph->{$clause_node_id}->{'adj'}->@*, $next_id;

            # Continue search with new clause node.
            connect_conjunctions($graph, $clause_graph, $next_id, $next_id);
        } else {
            # Add word to clause node's word list.
            push $clause_graph->{$clause_node_id}->{'word_ids'}->@*, $next_id;

            # Continue searching with this clause node.
            connect_conjunctions($graph, $clause_graph, $clause_node_id, $next_id);
        }
    }
}

sub combine_adj($graph, $clause_graph, $id) {
    my @new_adj;
    my @adj = get_adj($clause_graph, $id);

    for my $adj_id (@adj) {
        my @adj2 = get_adj($clause_graph, $adj_id);
        for (@adj2) {
            push @new_adj, $_;
            $clause_graph->{$_}->{'parent_id'} = $id;
        }
        push $clause_graph->{$id}->{'word_ids'}->@*, $clause_graph->{$adj_id}->{'word_ids'}->@*;
        delete $clause_graph->{$adj_id};
    }
    $clause_graph->{$id}->{'adj'}->@* = @new_adj;
}

# Search through clause nodes (i.e. conjunction words) in the clause graph recursively and combine nodes which correspond to list structures.
sub detect_list_structures($graph, $clause_graph, $id) {
    my @adj = get_adj($clause_graph, $id);
    if (@adj == 0) {
        # Stop search if arrived at leaf node.
        return;
    } elsif (@adj == 1) {
        if (Word::is_verb(Graph::get_word($graph, $adj[0]))) {
            # Continue search if links to a verbal conjunction.
            detect_list_structures($graph, $clause_graph, $adj[0]);
        } else {
            # Combine non-verbal conjunction to this node.
            combine_adj($graph, $clause_graph, $id);

            # Search this node again after combining adj.
            detect_list_structures($graph, $clause_graph, $id);
        }
    } else {
        my @verbs = grep { Word::is_verb(Graph::get_word($graph, $_)) } @adj;

        if (@verbs) {
            # ?
            detect_list_structures($graph, $clause_graph, $_) for @adj;
        } else {
            # Combine non-verbal conjunctions which indicate a list structure.
            combine_adj($graph, $clause_graph, $id);

            # Search this node again after combining adj.
            detect_list_structures($graph, $clause_graph, $id);
        }
    }
}

sub clause_graph($graph) {
    my $root_id = Graph::get_root_id($graph);
    my %clause_graph = (
        'root' => $root_id,
        $root_id => clause_node($root_id, undef)
    );

    connect_conjunctions($graph, \%clause_graph, $root_id, $root_id);

    detect_list_structures($graph, \%clause_graph, $root_id);

    return %clause_graph;
}

# Accessors.
sub get_adj($clause_graph, $id) { return $clause_graph->{$id}->{'adj'}->@*; }
sub get_sorted_clause_node_ids($clause_graph) { return Utils::intsort grep { /\d+/ } keys %$clause_graph; }
sub get_sorted_word_ids($clause_graph, $clause_node_id) { return Utils::intsort $clause_graph->{$_}->{'word_ids'}->@*; }

1;
