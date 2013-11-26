##
#Takes alameda county data and then strips all of the excess from it
#Spits out the data into a file called clean_data.csv
#
##
#!/usr/bin/perl

open (MYFILE, 'Alameda_County_Sheriff_Crime_Reports.csv');
$count=0;
open (OUTPUT, '>clean_data.csv');
print OUTPUT "Latitude, Longitude, Zip Code, City, Description \n";
while (<MYFILE>) {
	chomp;
	my @values = split(',', $_);
	print "$values[9], $values[10], $values[4], $values[2],$values[6]\n";
	if($count>=1){
	$values[9] =~ s/[^0-9.]//g;
	$values[10] =~ s/[^0-9.]//g;
	$values[9]= sprintf("%.3f", $values[9] );
	$values[10]=sprintf("%.3f", $values[10]);
	print OUTPUT "$values[9], $values[10], $values[4], $values[2], $values[6] \n";
 	#print "$_\n";
	}
	$count++;
}
close (MYFILE); 
close(OUTPUT);
