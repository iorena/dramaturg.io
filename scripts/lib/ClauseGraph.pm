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

# ClauseGraph assembles the sentence text into (clause) nodes that contain exclusive lists of words
# and then connects the nodes together. However, the interpretation of "clause" is extended as needed
# to suit the functionality of this program and as such might not match any real-world definitions of what a clause is.

package ClauseGraph;

sub clause_node($word_id, $parent_id) {
    return {
        'word_id' => $word_id,
        'parent_id' => $parent_id,
        'word_ids' => [$word_id],
        'adj' => []
    };
}

# Recursive DFS through the dependency graph which constructs and connects new clause nodes at conjunction words.
sub construct_clause_graph($graph, $clause_graph, $clause_node_id, $id) {
    for my $next_id (Graph::get_radj_ids($graph, $id)) {
        if (Conjunction::is_conjunction_word($graph, Graph::get_word($graph, $next_id))) {
            # Word is conjunction: create new clause node.
            $clause_graph->{$next_id} = clause_node($next_id, $clause_node_id);

            # Connect new clause node to parent.
            push $clause_graph->{$clause_node_id}->{'adj'}->@*, $next_id;

            # Continue search with new clause node.
            construct_clause_graph($graph, $clause_graph, $next_id, $next_id);
        } else {
            # Add word to clause node's word list.
            push $clause_graph->{$clause_node_id}->{'word_ids'}->@*, $next_id;

            # Continue searching with this clause node.
            construct_clause_graph($graph, $clause_graph, $clause_node_id, $next_id);
        }
    }
}

# Merge a clause node with its children.
sub merge_adj($graph, $clause_graph, $id) {
    my @adj;

    for my $adj_id (get_adj($clause_graph, $id)) {
        # Get child's children.
        my @adj2 = get_adj($clause_graph, $adj_id);

        # They will be the clause node's new children.
        push @adj, @adj2;
        $clause_graph->{$_}->{'parent_id'} = $id for @adj2;

        # Copy word_ids.
        push $clause_graph->{$id}->{'word_ids'}->@*, $clause_graph->{$adj_id}->{'word_ids'}->@*;

        # Delete child.
        delete $clause_graph->{$adj_id};
    }

    $clause_graph->{$id}->{'adj'}->@* = @adj;
}

# Merge clause nodes at adjacent levels if they correspond to list structures in the sentence.
sub detect_list_structures($graph, $clause_graph, $id) {
    my @adj = get_adj($clause_graph, $id);
    if (@adj == 0) {
        # Stop search if arrived at leaf node.
        return;
    } elsif (@adj > 0) {
        # Merge if the clause node is only adjacent to non-verbal conjunction words.
        if (grep { Word::is_verb(Graph::get_word($graph, $_)) } @adj) {
            # Contains any verbal conjunction words: continue search normally from all children.
            detect_list_structures($graph, $clause_graph, $_) for @adj;
        } else {
            # Merge non-verbal conjunctions which indicate a list structure.
            merge_adj($graph, $clause_graph, $id);

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

    # Recursive DFS through the dependency graph which constructs and connects new clause nodes at conjunction words.
    construct_clause_graph($graph, \%clause_graph, $root_id, $root_id);

    # Merge clause nodes at adjacent levels if they correspond to list structures in the sentence.
    detect_list_structures($graph, \%clause_graph, $root_id);

    return %clause_graph;
}

# Accessors.
sub get_adj($clause_graph, $id) { return $clause_graph->{$id}->{'adj'}->@*; }
sub get_sorted_clause_node_ids($clause_graph) { return Utils::intsort grep { /\d+/ } keys %$clause_graph; }
sub get_sorted_word_ids($clause_graph, $clause_node_id) { return Utils::intsort $clause_graph->{$clause_node_id}->{'word_ids'}->@*; }

1;
