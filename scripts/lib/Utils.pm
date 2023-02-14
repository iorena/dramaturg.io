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

sub word_ids_to_text($graph, @ids) { return ("\"" . join(" ", map { Word::form(Graph::get_word($graph, $_)) } intsort @ids) . "\"") =~ s/\s+([,.;:!?])/$1/gr; }

sub remove_hashtag($str) { return $str =~ s/#//gr; }

sub lower_case($str) { return Encode::encode("utf-8", lc Encode::decode("utf-8", $str)); }

1;
