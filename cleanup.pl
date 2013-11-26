#!/usr/bin/perl
#opens file and cleans up into a new file
open (MYFILE, 'Alameda_County_Sheriff_Crime_Reports.csv');
$count=0;
open (OUTPUT, '>clean_data.csv');
print OUTPUT "Latitude, Longitude, Zip Code, City, Description \n";
while (<MYFILE>) {
	chomp;
	my @values = split(',', $_);
	#print "$values[9], $values[10], $values[4], $values[2],$values[6]\n";
	if($count>=1){
	$values[9] =~ s/[^0-9.]//g;
	$values[10] =~ s/[^0-9.]//g;
	$values[9]= sprintf("%.3f", $values[9] );
	$values[10]=sprintf("%.3f", $values[10]);
	print OUTPUT "$values[9], $values[10], $values[4], $values[2] \n";
 	#print "$_\n";
	}
	$count++;
}
close (MYFILE); 
close(OUTPUT);
#clustering data
open (MYFILE, 'clean_data.csv');
$count = 0;
$inner = 0;
while(<MYFILE>){
	chomp;
	@lines[$count] = "$_\n";
#	while($inner<=$count){
#		my @glob = split(',', $lines[$count]);
#		my @curr = split(',', $lines[$inner]);
#		$inner++;
#	}
#	$inner=0;
	print "$lines[$count]";

	$count++;
}
@lines = sort { # Compare second fields
    (split',' , $a)[1]
    cmp
    (split " ", $b)[1]
} @lines;
close(MYFILE);

