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
use ActionTypePostProcessor;
use Document;
use DocumentParser;
use Log;
use Output;

my $execname = "action_type_parser";
die "$execname: no arguments provided.\n" unless @ARGV;

# Set names for logging and clear log file.
$Log::execname = $execname;
$Log::logfile = "$dirname/$execname.log";
$Output::execname = $execname;
Log::clear_log();

# Read document filepaths from command line arguments.
my @documents = Document::prepare_documents(@ARGV);

DocumentParser::parse_documents(@documents);

for my $document (@documents) {
    Log::message("Processing document <" . $document->{'filename'} . ">\n");

    # Parse action types.
    ActionTypeParser::parse_action_types($document, $_) for Document::get_sentences($document);
}

my @action_types = ActionTypePostProcessor::post_process_action_types(@documents);

Output::print_action_type_headers();
Output::print_action_types($_) for sort { $a->{'action_type_id'} cmp $b->{'action_type_id'} } @action_types;

Log::message("Output " . scalar(@action_types) . " action types.\n");

Log::message("Done.");

