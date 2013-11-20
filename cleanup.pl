#!/usr/bin/perl
open (MYFILE, 'Alameda_County_Sheriff_Crime_Reports.csv');
while (<MYFILE>) {
	chomp;
 	print "$_\n";
 }
 close (MYFILE); 
