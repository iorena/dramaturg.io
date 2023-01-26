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
use Output;
use ProjectWordsParser;

my $execname = "project_words_parser";
die "$execname: no arguments provided.\n" unless @ARGV;

# Set names for logging and clear log file.
$Output::execname = $execname;
$Output::logfile = "$dirname/$execname.log";
Output::clear_log();

# Read document filepaths from command line arguments.
my @documents = Document::prepare_documents(@ARGV);

DocumentParser::parse_documents(@documents);

for my $document (@documents) {
    Output::log_msg("Processing document <" . $document->{'filename'} . ">\n");

    # Parse project words.
    ProjectWordsParser::parse_project_words($document, $_) for Document::get_sentences($document);
}

my @project_words = sort { $a->{'score'} <=> $b->{'score'} } map { Document::get_project_words($_) } @documents;

Output::print_project_words(@project_words);

my $n_project_words = 0;
$n_project_words += scalar(Document::get_project_words($_)) for @documents;

Output::log_msg("Done. Parsed $n_project_words project words.");

