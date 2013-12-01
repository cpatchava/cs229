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
	if($count>0){
	$values[8] =~ s/[^0-9.-]//g;
	$values[9] =~ s/[^0-9.-]//g;
	$values[8]= sprintf("%.3f", $values[8] );
	$values[9]=sprintf("%.3f", $values[9]);
	print OUTPUT "$values[8], $values[9], $values[4], $values[2], $values[11], 1 \n";
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
while(<MYFILE>){#take all of the info and put it into an array
	chomp;
	#print "$_\n";
	#if($count <= 50){
	@lines[$count] = "$_\n";
	$count++;
	#print $lines[$count-1];
	#if(count>30){
	#	break;
	#}
	#}
}

$curr_max=1;
$match =0;
@clustered_set[0] = $lines[0];
@clustered_set[1] = $lines[1];
print "\n";
for($i=1;$i<$count;$i++){
	my @global_line = split(',' , $lines[$i]);#this is the current global output value
	$j=1;
	
	
	while($j<=$i){
		@cline = split(',', $clustered_set[$j]);
		if($global_line[0] eq $cline[0]){
			$cline[5]++;
			@clustered_set[$j] = "$cline[0],$cline[1],$cline[2],$cline[3],$cline[4],$cline[5]\n";
			$match=1;
		#	print "$clustered_set[$j]";
			break;
		}
		$j++;
	}

	if($match == 0){
		$curr_max++;
		@clustered_set[$curr_max] = "$global_line[0],$global_line[1],$global_line[2],$global_line[3],$global_line[4],$global_line[5]";
		#print "$clustered_set[$curr_max] \n";
	}
#	print "$curr_max,";
	$match=0;	
}
	$inner=0;
	print "$lines[$count]";

close(MYFILE);
$count = 0;
while($count <= $curr_max){
	print CROPPED "$clustered_set[$count]";
	$count++;
}

close(CROPPED);
print "The trimmed data is in data_crop.csv\n";
