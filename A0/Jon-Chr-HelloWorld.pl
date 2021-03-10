$| = 1;
use strict;
use warnings;
use diagnostics;

print "Hello World!\n";

my $filename = $ARGV[0];

if ($filename eq "")
{
    print "No filename was given!\n";
}


open(FH, '<', $filename) or die("Cannot open $filename");

while (<FH>)
{
    print $_;
}

close(FH);



