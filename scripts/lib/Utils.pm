#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use locale;

use File::Basename;
use lib dirname (__FILE__);

use Graph;
use Word;

use Encode qw(encode decode);

package Utils;

sub intsort(@values) { return sort { $a <=> $b } @values; }

sub precision($x, $p) { return int($x * (10 ** $p) + 0.5) / (10 ** $p); }

sub average(@vals) {
    my $avg = 0;
    my $n = scalar(@vals);
    $avg += $_ for @vals;
    return $n > 0 ? $avg / $n : 0;
}

sub contains($array, @keys) {
    for my $key (@keys) {
        return 1 if grep { $_ == $key } $array->@*;
    }
    return 0;
}

# Convert a list of words into a text string of their CoNLL-U forms. The words are space-separated with the exception of puncutations.
sub word_ids_to_text($graph, @word_ids) { return join(" ", map { Word::form(Graph::get_word($graph, $_)) } intsort @word_ids) =~ s/\s+([,.;:!?])/$1/gr; }

# Get CoNLL-U forms with quotes wrapped around each word.
sub list_word_forms_quoted(@words) { return join(", ", map { "\"" . Word::form($_) . "\"" } sort { Word::id($a) <=> Word::id($b) } @words); }

# Remove hashtags from a string (typically hashtags separated compound word parts in CoNLL-U lemmas).
sub remove_hashtag($str) { return $str =~ s/#//gr; }

# Proper conversion of UTF-8 strings to lower case.
sub lower_case($str) { return Encode::encode("utf-8", lc Encode::decode("utf-8", $str)); }

1;
