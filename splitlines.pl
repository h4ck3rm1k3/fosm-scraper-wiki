use lib "../Archive--Zip--Streaming--Write";
use lib "../Archive--Zip--Build";
use Archive::Zip::Streaming::Write;
my $file =shift;
my $ofile =shift;

my $fh;
my $ifh;
open($fh, ">$ofile");
open($ifh, "<$file");

print "$ofile $file\n";
my $z=Archive::Zip::Streaming::Write->new($fh);
my ($filename,$mode) = ("test",777);

my $t=time();
$atime= $mtime=$ctime=$t;

while(<$ifh>) {
    if (/id='(\d+)'/){
	my $id=$1;
	my @chars = split "",$id;
	my $path=join "/",@chars;
#	print $_;
	$z->add_file("$path/d",$_, $atime, $mtime, $ctime, $mode);	
    }
}
close IN;
$z->close();
close $fh;
