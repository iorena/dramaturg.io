#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

use Score;

package Document;

our $running_document_id = 0;

# Initialize new document.
sub document($filepath, $filename) {
    return {
        'filepath' => $filepath,
        'filename' => $filename,
        'document_id' => ++$running_document_id,
        'score_keeper' => Score::score_keeper(),
        'sentences' => [],
        'action_types' => [],
        'project_words' => []
    };
}

sub prepare_documents(@ARGV) { return map { document($_, (File::Basename::fileparse($_, qr/\.[^.]*/))[0]) } @ARGV; }

sub get_sentences($document) { return $document->{'sentences'}->@*; }

sub get_action_types($document) { return $document->{'action_types'}->@*; }

sub get_project_words($document) { return $document->{'project_words'}->@*; }

1;
