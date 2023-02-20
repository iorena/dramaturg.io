#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

my $dirname;
BEGIN {
    use File::Basename;
    $dirname = dirname($0);
}
use lib "$dirname/lib";

use Document;
use DocumentParser;
use Log;
use Output;
use ProjectWordsParser;

my $execname = "project_words_parser";
die "$execname: no arguments provided.\n" unless @ARGV;

# Set names for logging and clear log file.
Log::open_and_clear_log($execname, "$dirname/$execname.log");
$Output::execname = $execname;

# Read document filepaths from command line arguments.
my @documents = Document::prepare_documents(@ARGV);

DocumentParser::parse_documents(@documents);

for my $document (@documents) {
    Log::write_out("Processing document <" . $document->{'filename'} . ">\n");

    # Parse project words.
    ProjectWordsParser::parse_project_words($document, $_) for Document::get_sentences($document);
}

my @project_words = reverse sort { $a->{'score'} <=> $b->{'score'} } map { Document::get_project_words($_) } @documents;

Output::print_project_words(@project_words);

my $n_project_words = 0;
$n_project_words += scalar(Document::get_project_words($_)) for @documents;

Log::write_out("Done. Parsed $n_project_words project words.");

