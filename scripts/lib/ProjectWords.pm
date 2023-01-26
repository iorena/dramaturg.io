#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

package ProjectWords;

our @project_words_field_names = (
    'subject',
    'verb',
    'object',
    'object_case',
    'score'
);

# Initialize blank project word. Note that 'subject', 'verb' and 'object' are word hashes.
sub project_words() {
    return { map { $_ => "NONE" } @project_words_field_names };
}

1;
