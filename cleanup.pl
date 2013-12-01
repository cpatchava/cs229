#!/usr/bin/perl
#system('new_program.pl');
#opens file and cleans up into a new file
open (MYFILE, 'Undisturbing_data.csv');
$count=0;
open (OUTPUT, '>clean_data.csv');
print OUTPUT "Latitude, Longitude, Zip Code, City, Description, count \n";
while (<MYFILE>) {
	chomp;
	my @values = split(',', $_);
	#print "$values[9], $values[10], $values[4], $values[2],$values[6]\n";
	if($count>=0){
	$values[8] =~ s/[^0-9.-]//g;
	$values[9] =~ s/[^0-9.-]//g;
	$values[8]= sprintf("%.3f", $values[8] );
	$values[9]=sprintf("%.3f", $values[9]);
	print OUTPUT "$values[8], $values[9], $values[4], $values[2], $values[10], 1 \n";
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
open (CROPPED, '>data_crop.csv');
while(<MYFILE>){
	chomp;
	@lines[$count] = "$_\n";
	#my @lines = split(',', $_);
	while($inner<=$count){
		my @glob = split(',', $lines[$count]);
		my @curr = split(',', $lines[$inner]);
		$inner++;
		for($i=0; $i < 7; $i++){

			if($glob[0] eq $curr[0]){
			print CROPPED "$glob[$i],";	
			}
		
		}
	}
	$inner=0;
	print "$lines[$count]";

	$count++;
}
close(MYFILE);
close(CROPPED);
