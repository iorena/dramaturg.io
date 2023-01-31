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
use Score;
use Output;
use Word;

package DocumentParser;

# Parse word lines from all the "text" entries in the document.
sub parse_text($document) {
    local $_; # Prevent overwriting global $_.

    my $filepath = $document->{'filepath'};
    open(my $fh, '<', $filepath) or die "$Output::execname: no such file '$filepath'";

    # Read all sentences from CoNLL-U formated standard input text.
    # Word lines come after the '#text' entry.
    # The first word line field is the ID field, represented by an integer.
    # Multi-id lines (whose ID is of the type 8-9 etc) will be skipped -- their data is given separately.
    while (<$fh>) {
        next unless /^# text = (.*)/;
        my $sentence = Sentence::sentence($1);

        # Skip remaining comment lines until we reach the start of the word lines. Also skips multi-id lines.
        while (<$fh>) {
            die "$Output::execname: could not parse word lines" if /^# text =/; # Should not reach next 'text' without reading any word lines.
            last if /^\d+\s/;
        }
        Sentence::add_word($sentence, Word::parse_word_line($_));

        # Parse remaining word lines.
        while (<$fh>) {
            last unless /^\d+/;
            Sentence::add_word($sentence, Word::parse_word_line($_)) if /^\d+\s/;
        }

        push $document->{'sentences'}->@*, $sentence;
    }
    close($fh) or die "$Output::execname: could not close file '$filepath'";
}

sub parse_documents(@documents) {
    for my $document (@documents) {
        # Parse document text.
        DocumentParser::parse_text($document);

        # Count all words in the document for scoring.
        Score::add_word_counts($document, $document->{'score_keeper'});
        Score::add_word_counts($document, $Score::global_score_keeper);
    }
}

1;
