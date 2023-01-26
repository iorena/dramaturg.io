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

# Create a graph node hash, which at first only contains the stored word hash.
# 'radj' is the list of neighbors (as word hashes) in the reverse graph.
sub node($word) {
    return {
        'word' => $word,
        'radj' => []
    };
}

# Create a graph hash.
# Word ids will be keys for the graph nodes except for the special key 'root' which stores the root graph node's id.
sub graph($sentence) {
    my @words = Sentence::get_words($sentence);

    # Create a node in the graph for each word in the sentence.
    my %graph = map { Word::id($_) => node($_) } @words;

    # Create lists of neighbors in the reverse graph.
    push $graph{Word::head($_)}->{'radj'}->@*, $_ for @words;

    # Store root node's id separately.
    $graph{'root'} = Word::id($graph{0}->{'radj'}[0]);

    return %graph;
}

# Accessors for the graph.
sub get_root_id($graph) { return $graph->{'root'}; }
sub get_word($graph, $id) { return $graph->{$id}->{'word'}; }
sub get_radj($graph, $id) { return $graph->{$id}->{'radj'}->@*; }
sub get_radj_ids($graph, $id) { return map { Word::id($_) } get_radj($graph, $id); }

# Get radj for which the predicate returns true.
sub get_radj_if($graph, $id, $predicate) { return grep { $predicate->($_) } get_radj($graph, $id); }
sub get_radj_ids_if($graph, $id, $predicate) { return map { Word::id($_) } get_radj_if($graph, $id, $predicate); }

1;
