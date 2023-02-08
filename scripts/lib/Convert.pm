#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

package Convert;

our %convert_mood = (
    'Imp' => 'IMPV',
    'Ind' => 'INDV',
    'Inf' => 'INF',
    'Cnd' => 'COND'
);

our %convert_tense = (
    'Pres' => 'prees',
    'Past' => 'imperf',
    'Perf' => 'perf',
    'Pluperf' => 'pluperf'
);

our %convert_person = (
    '1' => 'Speaker',
    '2' => 'Listener'
);

sub tense($tense) { return exists $convert_tense{$tense} ? $convert_tense{$tense} : $tense; }
sub mood($mood) { return exists $convert_mood{$mood} ? $convert_mood{$mood} : $mood; }
sub person($person) { return exists $convert_person{$person} ? $convert_person{$person} : $person; }

1;
