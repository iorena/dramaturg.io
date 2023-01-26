#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

use Document;
use Graph;
use Sentence;
use Utils;
use Word;

package Score;

# Stores word occurrences in the document(s).
sub score_keeper() {
    return {
        'word_counts' => {}
    };
}

our $global_score_keeper = score_keeper();

# Count all the words in the document. In case of compound words, each word part is treated separately.
sub add_word_counts($document, $score_keeper) {
    for my $sentence (Document::get_sentences($document)) {
        for my $word (Sentence::get_words($sentence)) {
            ++$score_keeper->{'word_counts'}->{$_} for Word::get_word_parts($word);
        }
    }
}

# Compound words are treated as the average of their parts.
sub score_word($score_keeper, $word) {
    my @parts = Word::get_word_parts($word);
    my $score = 0;
    $score += $score_keeper->{'word_counts'}->{$_} for @parts;
    return $score / @parts;
}

# Score a list of words such that only nouns and proper nouns count for the score.
sub score_words($score_keeper, @words) {
    my ($n, $score) = (0) x 2;
    for my $word (@words) {
        if (Word::is_noun($word) || Word::is_propn($word)) {
            $score += score_word($score_keeper, $word);
            ++$n;
        }
    }
    return $n > 0 ? $score / $n : 0;
}

1;
