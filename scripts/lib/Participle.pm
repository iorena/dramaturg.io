#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

use Word;

package Participle;

# Accept only past participles II (NUT) and V (TU).
sub check_proper_participle($word) {
    my ($partform, $verbform) = Word::get_feats($word, ("PartForm", "VerbForm"));
    if ($verbform eq "Part") {
        return 0 if $partform eq "Pres"; # I (VA) and IV (VA) present participles.
        return 0 if $partform eq "Agt"; # III (MA) agent participle.
        return 0 if $partform eq "Neg"; # IV negative participle.
    }
    return Word::is_verb($word);
}

1;
