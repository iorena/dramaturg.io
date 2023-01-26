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

use ActionTypeParser;
use Document;
use DocumentParser;
use Output;

my $execname = "action_type_parser";
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

    # Parse action types.
    ActionTypeParser::parse_action_types($document, $_) for Document::get_sentences($document);
}

Output::print_action_type_headers();
Output::print_action_types(Document::get_action_types($_)) for @documents;

my $n_action_types = 0;
$n_action_types += scalar(Document::get_action_types($_)) for @documents;

Output::log_msg("Done. Parsed $n_action_types action types.");

