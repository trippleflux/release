#!/usr/bin/perl -w

# Script to read test results stored in files from a given list of 
# files and save results in database, with date and time 
# when executed. 
#
# Author: Sachin Kumar <skumar1@novell.com>

use XML::DOM;
use DBI;

$DATE = `date +'%Y%m%d'`;
chomp $DATE ;

$MCS_ROOT = "/tmp/snapshot/$DATE/mcs";
#$MCS_ROOT = shift ;
$TESTFILES_ROOT = "/var/www/html/tests/$DATE" ;

$TESTPASS = 0;
$TESTFAIL = 1;
$TESTNOTRUN = 2; 

# Types of tests
$NUNITTESTS = 0 ;
$MCSTESTS = 1 ;
$RUNTIMETESTS = 2 ;

$DATETIME=`date +'%Y-%m-%d %H:%M:%S'` ;
chomp $DATETIME ;

# Set the parameter values for the connection

$databaseName = "DBI:mysql:test";
$databaseUser = "root";
$databasePw = "";

$dbh = DBI->connect($databaseName, $databaseUser, 
		    $databasePw) || die "Connect failed: $DBI::errstr\n";


@MCS_NUNIT_TESTDIRS = (
		       "$MCS_ROOT/class/Commons.Xml.Relaxng",
		       "$MCS_ROOT/class/Cscompmgd",
		       "$MCS_ROOT/class/Microsoft.JScript",
		       "$MCS_ROOT/class/Microsoft.VisualBasic",
		       "$MCS_ROOT/class/Mono.Directory.LDAP",
		       "$MCS_ROOT/class/Mono.Security",
		       "$MCS_ROOT/class/Mono.Security.Win32",
		       "$MCS_ROOT/class/Npgsql",
		       "$MCS_ROOT/class/System",
		       "$MCS_ROOT/class/System.Configuration.Install",
		       "$MCS_ROOT/class/System.Data",
		       "$MCS_ROOT/class/System.Drawing",
		       "$MCS_ROOT/class/System.Runtime.Remoting",
		       "$MCS_ROOT/class/System.Runtime.Serialization.Formatters.Soap",
		       "$MCS_ROOT/class/System.Security",
		       "$MCS_ROOT/class/System.Web.Services",
		       "$MCS_ROOT/class/System.XML",
		       "$MCS_ROOT/class/corlib"
		       );

@MCS_COMPILER_TESTFILES = (
			   "$TESTFILES_ROOT/mcstests",
			   "$TESTFILES_ROOT/mcserrortests",
			   "$TESTFILES_ROOT/mbastests"  
			   );

@MCS_SUCCESS_CODES = (
		      "OK",
		      "SUCCESS",
		      "OK"
		      );

@MCS_ERROR_CODES = (
		    "FAILED",
		    "ERROR",
		    "FAILED"
		    );


@MONO_RUNTIME_TESTFILES = (
			   "$TESTFILES_ROOT/monotests",
			   "$TESTFILES_ROOT/minitests"
			   );

# Scan all files (TestResult.xml)  generated by nunit

for ( @MCS_NUNIT_TESTDIRS )
{
    my $parser = new XML::DOM::Parser;
    my $doc = $parser->parsefile ( $_."/TestResult.xml" ) ;
    
    # get testsuite results, for tests executed.
    my $ts_results = get_nunit_testsuite_results ( $doc ) ;

    my @arr = split ('/', @$ts_results[0]); # split to get testsuite name    
    
    # get data for each test case run
    my $tcresults = get_testcase_results ($doc) ;

    my $tsexectime = 0 ;
    $tsexectime += $_->[4]
	foreach @$tcresults;

    # Store the results in db, with current time and date 
    store_testsuite_results ( $ts_results, $NUNITTESTS, $tsexectime ) ;

    # Store the results in db, with current time and date 
    store_testcase_results ( $tcresults, $arr[$#arr]) ;
    
    $doc->dispose ;
}


# Scan all Compiler tests result files

my $k = 0 ;
for ( @MCS_COMPILER_TESTFILES )
{
    my $ts_results = get_compiler_test_results ( $_ , $MCS_SUCCESS_CODES[$K], $MCS_ERROR_CODES[$K] ) ;
    $K++ ;
    # Store results in database with current date and time
    store_testsuite_results ( $ts_results, $MCSTESTS, 0 ) ;
}

# Scan all mono runtime test files

for ( @MONO_RUNTIME_TESTFILES )
{
    my $ts_results = get_runtime_test_results ( $_ , "pass", "failed" ) ;
    
    # Store results in database with current date and time
    store_testsuite_results ( $ts_results, $RUNTIMETESTS, 0 ) ;
}

sub get_runtime_test_results
{
    my ( $testresult, $PASS, $FAIL ) = @_ ;
    my @tsresults = ($testresult, 0, 0, 0) ;
    
    open (FILEHANDLE, $testresult);
    if ( $testresult =~ /minitests/ )
    {
	while (<FILEHANDLE>) 
	{
	    if( /^Results/ ) 
	    {
		my @arr = split (' ', $_);
		$arr[3] = substr ($arr[3], 0, -1);
		$arr[5] = substr ($arr[5], 0, -1);
		$tsresults[1] += ($arr[3] - $arr[5]) ;
		$tsresults[2] += $arr[5] ;
	    }
	    
	}
    }
    else
    {
	while (<FILEHANDLE>) 
	{
	    $tsresults[1]++ if /$PASS/ ;
	    $tsresults[2]++ if /$FAIL/ ;
	}
    }
    
    return \@tsresults ;
    
}

sub get_compiler_test_results
{
    my ( $testresult, $PASS, $FAIL ) = @_ ;
    my @tsresults = ($testresult, 0, 0, 0) ;
    
    open (FILEHANDLE, $testresult);
    
    while (<FILEHANDLE>) 
    {
	$tsresults[1]++ if /$PASS/ ;
	$tsresults[2]++ if /$FAIL/ ;
    }
    
    return \@tsresults ;
}


sub get_nunit_testsuite_results
{
    my $doc = shift ;
    my @attrs = ( 'name', 'total', 'failures', 'not-run' ) ;
    my @tsresults = () ;
    
    my $nodes = $doc->getElementsByTagName ("test-results");
    my $len = $nodes->getLength;
    
    if($nodes->getLength != 1)
    {
	print "Unexpected doc: may have more number of test-result tags";
	return \@tsresults;
    }
    
    my $node = $nodes->item ( 0 );
    my $i = 0 ;
    for (@attrs)
    {
	my $n = $node->getAttributeNode ( $_ ) ;
	$tsresults[$i++] = $n->getValue ;
    }
    
    $tsresults[1] -= $tsresults[2] ; # pass = total - fail 
    return \@tsresults;
}   

sub get_testcase_results
{
    my $doc = shift ;
    my @attrs = ( 'name', 'executed', 'success', 'time' ) ;
    my @tcresults = () ;
    
    my $tcname ;        # list contains names of each testcase
    my $tcstatus ;     # status: pass, fail, not run
    my $tcmessage ;    # messages for each test case, if any, else empty
    my $tcstacktrace ; # stack traces for each test case, else empty
    my $tcexectime ;
    
    for my $node ($doc->getElementsByTagName ("test-case"))
    {
	# intializing with default values
	$tcexectime = 0 ;
	$tcmessage = "" ;
	$tcstacktrace = "" ;
	
	$tcname = ($node->getAttributeNode($attrs[0]))->getValue ;
	if(($node->getAttributeNode($attrs[1]))->getValue ne "False")
	{
	    if(($node->getAttributeNode($attrs[2]))->getValue eq "False")
	    {
		$tcstatus = $TESTFAIL ;
		
		my $msglist = $node->getElementsByTagName ("message");
		my $msg = $msglist->item(0) ;

		my $stlist = $node->getElementsByTagName ("stack-trace");
		my $st = $stlist->item(0) ;
		if ( $st->hasChildNodes == 1)
		{
		    $tcstacktrace = ($st->getFirstChild)->getNodeValue ;
		}
		push @tcresults, [ $tcname, $TESTFAIL, ($msg->getFirstChild)->getNodeValue, $tcstacktrace, $tcexectime ];
	    }
	    
	    else
	    {
		push @tcresults, [ $tcname, $TESTPASS, "", "", ($node->getAttributeNode ($attrs[3]))->getValue ];
	    }
	}
	else
	{
	    my $msglist = $node->getElementsByTagName ("message");
	    my $msg = $msglist->item(0) ;
	    push @tcresults, [ $tcname, $TESTNOTRUN, ($msg->getFirstChild)->getNodeValue, "", $tcexectime ];
	}
    }
    return \@tcresults ;
}   


sub store_testsuite_results
{
    my $tsresults = shift ;
    my $type = shift ; 
    my $tsexectime = shift ;
    
    my @arr = split ('/', @$tsresults[0]);
     
    # Removing _test.dll from the testsuite name
    $arr[$#arr] =~ s/_test.dll$//g ; 
    
    my $logfile = "" ;
    if ( $type == $MCSTESTS || $type == $RUNTIMETESTS )
    {
	$logfile = "$arr[$#arr -1]/$arr[$#arr]" ;
    }
    
    my $stmt = "INSERT INTO testsuite VALUES ('$arr[$#arr]', @$tsresults[1] , @$tsresults[2], @$tsresults[3], $tsexectime, '$logfile', $type, '$DATETIME')" ;
    print $stmt. "\n" ;
    
    # Prepare and execute the SQL query
    my $sth = $dbh->prepare($stmt) 
	|| die "prepare: $$stmt: $DBI::errstr";
    $sth->execute || die "execute: $$stmt: $DBI::errstr";
    
    # Clean up the record set
    $sth->finish();   
}


sub store_testcase_results
{
    my ($tcresults, $tsname) = @_ ;
    $tsname =~ s/_test.dll$//g ;

    foreach ( @$tcresults )
    {
	$_->[2]  =~ s/'/\\'/g ; # replacing ' with \' in message
	$_->[3]  =~ s/'/\\'/g ; # replacing ' with \' in stack trace
	
	my $stmt = "INSERT INTO testcase VALUES ('$_->[0]', '$tsname', $_->[1], '$_->[2]', '$_->[3]', $_->[4], '$DATETIME')" ;
	print $stmt. "\n" ;
	
	# Prepare and execute the SQL query
	my $sth = $dbh->prepare($stmt) 
	    || die "prepare: $$stmt: $DBI::errstr";
	$sth->execute || die "execute: $$stmt: $DBI::errstr";
	
	# Clean up the record set
	$sth->finish();   	
    }
}
