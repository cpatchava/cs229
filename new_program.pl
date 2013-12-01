#!/usr/bin/perl

open (MYFILE, 'final_set.csv');
open (MYOUT, '>Undisturbing_data.csv');
$count=0;
while (<MYFILE>) {
    chomp;
#	print "$_";
#    my (${date},${block},${city},${state},${zip},${cc},${aid},${cid},$loc,${blank},${loc}, ${lolz}) = split("]", $_);
	@vals = split("~", $_);
		for($i=0; $i<11; $i++){
			if($vals[6] eq "ACSO"){
    		print MYOUT "$vals[$i] ,";
			}
			else{
				if($i >= 6){
				print MYOUT "$vals[$i+1] ,";
				}
				else{
				print MYOUT "$vals[$i] ,";
				}
			}
	
		}
	print MYOUT "\n";
 
    $count++;
}

close(MYFILE);
