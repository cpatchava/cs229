#!/usr/bin/perl
#system('new_program.pl');
#opens file and cleans up into a new file
open (MYFILE, 'Undisturbing_data.csv');
$count=0;
open (OUTPUT, '>clean_data.csv');
print OUTPUT "Latitude, Longitude, Zip Code, City, Description, count, Block \n";
while (<MYFILE>) {
	chomp;
	my @values = split(',', $_);
	#print "$values[9], $values[10], $values[4], $values[2],$values[6]\n";
	if($count>0){
	$values[8] =~ s/[^0-9.-]//g;
	$values[9] =~ s/[^0-9.-]//g;
	$values[8]= sprintf("%.3f", $values[8] );
	$values[9]=sprintf("%.3f", $values[9]);
	print OUTPUT "$values[8], $values[9], $values[4], $values[2], $values[11], 1, $values[1] \n";
 	#print "$_\n";
	}
	$count++;
}
##################################################################################
close (MYFILE); 
close(OUTPUT);
#=pod
#clustering data
open (MYFILE, 'clean_data.csv');
$count = 0;
$inner = 0;
open (CROPPED, '>data_crop.csv');
while(<MYFILE>){#take all of the info and put it into an array
	chomp;
	@lines[$count] = "$_\n";
	$count++;
}

$curr_max=1;
$match =0;
@clustered_set[0] = $lines[0];
@clustered_set[1] = $lines[1];
print "\n";
for($i=1;$i<$count;$i++){
	my @global_line = split(',' , $lines[$i]);#this is the current global output value
	$j=1;
break;	
	
	while($j<=$i){
	#break;
		@cline = split(',', $clustered_set[$j]);
		if($global_line[0] eq $cline[0]){
			$cline[5]++;
			@clustered_set[$j] = "$cline[0],$cline[1],$cline[2],$cline[3],$cline[4],$cline[5]\n";
			$match=1;
		#	print "$clustered_set[$j]";
	#		break;
		}
		$j++;
	}

	if($match == 0){
		$curr_max++;
		@clustered_set[$curr_max] = "$global_line[0],$global_line[1],$global_line[2],$global_line[3],$global_line[4],$global_line[5]\n";
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
#=cut
#endif
print "The trimmed data is in data_crop.csv\n";
################################################################################################


open(ZIP, 'housing.csv');
my @zips;
my @outs;
$count=0;
while(<ZIP>){
    chomp;
    @zips[$count] = $_;
    $count++;
    @zline = split(',', $zips[$count-1]);
    if($zline[1] < 500000){
    $random_u= int(rand(350))+500;
    $random_e= int(rand(40))+40;

    }
    elsif($zline[1] > 500000 and $zline[1] < 750000){
    $random_u= int(rand(250))+400;
    $random_e= int(rand(50))+50;

    }
    elsif($zline[1] >750000 and $zline[1] < 950000){
    $random_u=  int(rand(50))+200;
    $random_e= int(rand(30))+70;

    }
    else{
    $random_u= int(rand(20))+50;
    $random_e= int(rand(5))+90;

    }
    $zip_house[$count -1] = "$zline[0],$zline[1],$random_u,$random_e \n";
        print "$zip_house[$count-1]";

}

close(ZIP);


################################################################################################
open(TOTAL, '>output.csv');
$final_total[0]= "Block, Primary Type, Description, Location, Description, Arrest, Domestic, Count, Latitude, Longitude, Unemployed, House, Education, Street_Crime, Label\n";
$c=0;
print "$zip_house[0]";
print "$zip_house[1]";
print "$zip_house[2]";

while($c <= $curr_max){
		@line =	split(',',$clustered_set[$c]);
		for($a=1; $a<$count; $a++){
		#	print "$zip_house[$a]";
			@zip_line = split(',',$zip_house[$a]);
			$line[2] =~ s/[^0-9.-]//g;
			$zip_line[0] =~  s/[^0-9.-]//g;
			#print"$line[2] -- $zip_line[0]\n";
			if($line[2] eq $zip_line[0]){
				$finale = int(rand(2));
				$line[5] =~ s/[^0-9.-]//g;
				$zip_line[2] =~ s/[^0-9.-]//g;
				@final_total[$c]="BLANK,BLANK,$line[3],Outside,$line[3],True,False,$line[5],$line[0],$line[1],$zip_line[2],$zip_line[1],$zip_line[2],$finale,$finale \n";
				break;
			}	
		}
	$c++;
}
###############################################################################################
print "size: $c curr max : $curr_max\n";
print "$final_total[0]";
print "$final_total[1]";
for($i=0; $i<$c; $i++){
	print TOTAL  "$final_total[$i]";
}

close(TOTAL);
