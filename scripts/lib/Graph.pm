#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

use Sentence;
use Word;

package Graph;

# Graph node hash which stores a word hash and a list of neighbors (as word hashes) in the reverse graph.
sub node($word) {
    return {
        'word' => $word,
        'radj' => [],
        'depth' => 0
    };
}

sub calculate_depths($graph, $id, $depth) {
    for (get_radj_ids($graph, $id)) {
        $graph->{$_}->{'depth'} = $depth;
        calculate_depths($graph, $_, $depth + 1);
    }
}

# Create dependency graph from a list of words where word ids are keys for the graph nodes.
# The special key 'root' points to the id of the lowest level node.
sub graph(@words) {
    # Create a node in the graph for each word in the sentence.
    my %graph = map { Word::id($_) => node($_) } @words;

    # Create lists of neighbors in the reverse graph.
    push $graph{Word::head($_)}->{'radj'}->@*, $_ for grep { exists $graph{Word::head($_)} } @words;

    # ConLL-U sentences should always be rooted with only one lowest level node.
    # Additionally, any other list of words passed to this subroutine follows a similar assumption.
    # In case of ambiguity caused by an error, a single root key will always be set here.
    my @root = map { Word::id($_) } grep { not exists $graph{Word::head($_)} } @words;
    $graph{'root'} = $root[0] if @root;

    calculate_depths(\%graph, $root[0], 1);

    return %graph;
}

# Accessors for the graph.
sub get_root_id($graph) { return $graph->{'root'}; }
sub get_word($graph, $id) { return $graph->{$id}->{'word'}; }
sub contains($graph, $id) { return exists $graph->{$id}; }
sub get_radj($graph, $id) { return $graph->{$id}->{'radj'}->@*; }
sub get_radj_ids($graph, $id) { return map { Word::id($_) } get_radj($graph, $id); }

# Get radj for which the predicate returns true.
sub get_radj_if($graph, $id, $predicate) { return grep { $predicate->($_) } get_radj($graph, $id); }
sub get_radj_ids_if($graph, $id, $predicate) { return map { Word::id($_) } get_radj_if($graph, $id, $predicate); }

1;
