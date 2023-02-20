#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

# Convert output into correct form.

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
    '2' => 'Listener',
    '3' => 'Character',
    '4' => 'me',
    '5' => 'te'
);

sub is_converted_person($value) { return scalar(grep { $_ eq $value } values %convert_person); }

our %convert_case = (
    'Nom' => 'NOM',
    'Acc' => 'AKK',
    'Gen' => 'GEN',
    'Ins' => 'INS',
    'Par' => 'PAR',
    'Ess' => 'ESS',
    'Tra' => 'TRA',
    'Com' => 'KOM',
    'Abe' => 'ABE',
    'Ine' => 'INE',
    'Ill' => 'ILL',
    'Ela' => 'ELA',
    'Ade' => 'ADE',
    'All' => 'ALL',
    'Abl' => 'ABL'
);

our %convert_number = (
    'Sing' => 'Yks',
    'Plur' => 'Mon'
);

sub tense($tense) { return exists $convert_tense{$tense} ? $convert_tense{$tense} : $tense; }
sub mood($mood) { return exists $convert_mood{$mood} ? $convert_mood{$mood} : $mood; }
sub person($person) { return exists $convert_person{$person} ? $convert_person{$person} : $person; }
sub case($case) { return exists $convert_case{$case} ? $convert_case{$case} : $case; }
sub number($number) { return exists $convert_number{$number} ? $convert_number{$number} : $number; }

sub generalize_subject($subject) { return is_converted_person($subject) ? $subject : "subject"; }
sub generalize_verb($verb) { return "project"; }
sub generalize_object($object) { return is_converted_person($object) ? $object : "object"; }

1;
