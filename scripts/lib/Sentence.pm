#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

package Sentence;

# Create a sentence hash, which at first only contains the raw text string.
# Processed word lines will be stored in the 'words' array as word hashes (see Word.pm).
sub sentence($text) {
    return {
        'text' => $1,
        'words' => []
    };
};

sub add_word($sentence, $word) { push $sentence->{'words'}->@*, $word; }

sub get_words($sentence) { return $sentence->{'words'}->@*; }

1;
