use lib "../Archive--Zip--Streaming--Write";
use lib "../Archive--Zip--Build";
use Archive::Zip::Streaming::Write;
my $file =shift;
my $ofile =shift;

my $fh;
open($fh, ">$ofile");
my $z=Archive::Zip::Streaming::Write->new($fh);
my ($filename,$mode) = ("test",777);

my $t=time();
$atime= $mtime=$ctime=$t;

open IN, "<" , $file;
while (<IN>)  {   
    chomp;
    my ($bucket,$block,$pos,$id)=split(",");#cache/xaaaa,datafiles/000001/node_ids.bin,0,321393880
#    $z->add_directory("$i", $atime, $mtime, $ctime, $mode);
    my @chars = split "",$id;
    my $path=join "/",@chars;
    $z->add_file("$path/d",$_, $atime, $mtime, $ctime, $mode);
}
close IN;
$z->close();
close $fh;
