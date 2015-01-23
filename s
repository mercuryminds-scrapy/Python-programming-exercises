 <?php
      $welcome = "Let's get started with PHP!";
      echo $welcome;
      ?>
    </h1></div>
    <p><strong>Generate a list:</strong>
      <?php
      for ($number = 1; $number <= 10; $number++) {
        if ($number <= 9) {
            echo $number . ", ";
        } else {
            echo $number . "!";
        }
      }; ?>
    </p>
    <p><strong>Things you can do:</strong>
      <?php
        $things = array("Talk to databases",
        "Send cookies", "Evaluate form data",
        "Build dynamic webpages");
        foreach ($things as $thing) {
            echo "<li>$thing</li>";
        }

        unset($thing);
      ?>




             //     echo "Oh, the humanity!";
    <?php
    $items=10;
    if($items >5){
    echo "You get a 10% discount!";
    }
    else
    {
        echo "dsdd";};
    ?>

      <?php
    switch (2) {
        case 0:
            echo 'The value is 0';
            break;
        case 1:
            echo 'The value is 1';
            break;
        case 2:
            echo 'The value is 2';
            break;
        default:
            echo "The value isn't 0, 1 or 2";
    }
    ?>



        <?php
    $i = 5;

    switch ($i) {
        case 0:
            echo '$i is 0.';
            break;
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
            echo '$i is somewhere between 1 and 5.';
            break;
        case 6:
        case 7:
            echo '$i is either 6 or 7.';
            break;
        default:
            echo "I don't know how much \$i is.";
    }
    ?>


    <?php
    $i = 5;

    switch ($i):
        case 0:
            echo '$i is 0.';
            break;
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
            echo '$i is somewhere between 1 and 5.';
            break;
        case 6:
        case 7:
            echo '$i is either 6 or 7.';
            break;
        default:
            echo "I don't know how much \$i is.";
    endswitch;
    ?>

     <?php
      $array = array("Egg", "Tomato", "Beans");
      echo $array[2]
    $languages = array("HTML/CSS",
        "JavaScript", "PHP", "Python", "Ruby");

        $languages[3]="impccc";
        echo $languages[3];
 $languages = array("HTML/CSS",
        "JavaScript", "PHP", "Python", "Ruby");
        // Write the code to remove Python here!

        unset($languages{3});

             foreach($languages as $lang) {
          print "<p>$lang</p>";
      ?>

  // Echoes the first five even numbers
       for ($i = 2; $i < 11; $i = $i + 2) {
          echo $i;




 	<?php
	$headCount = 0;
	$flipCount = 0;
	while ($headCount < 3) {
		$flip = rand(0,1);
		$flipCount ++;
		if ($flip){
			$headCount ++;
			echo "<div class=\"coin\">H</div>";
		}
		else {
			$headCount = 0;
			echo "<div class=\"coin\">T</div>";
		}
	}
	echo "<p>It took {$flipCount} flips!</p>";



	    $c=0;
    while($c<4):

        echo "<p>Iteration number: {$c}</p>";
        $c++;
    endwhile;



	?>




	<?php
	$flipCount = 0;
	do {
		$flip = rand(0,1);
		$flipCount ++;
		if ($flip){
			echo "<div class=\"coin\">H</div>";
		}
		else {
			echo "<div class=\"coin\">T</div>";
		}
	} while ($flip);
	$verb = "were";
	$last = "flips";
	if ($flipCount == 1) {
		$verb = "was";
		$last = "flip";
	}
	echo "<p>There {$verb} {$flipCount} {$last}!</p>";
	?>

	$length = strlen("david");
  print $length;



$d="anandhakumar";
echo substr($d,0,5);

echo strtoupper($d)
    echo strtolower($d)

    $n="anandha";
    echo strpos($n,"a");

        if (strpos($n,"g")==false)
    {
        echo "not there";
    }
    print round(M_PI, 3);
    $n="anandhakumar";



    echo $n[rand(0,strlen($n))];

       $a=array();
    array_push($a,"anand");


        $the_array=array(1,4,545,6,4,6,7,3);
    sort($the_array);
    print join(",", $the_array);
 rsort($the_array);
    print join(",",$the_array)


sudo -i -u postgres
 createdb mm

 psql
mm         postgres   template0  template1
postgres@MMTPC104:~$ psql -d mm


select * from mmtweet;
 create table mmtweet( id integer, username varchar(30), time timestamp, tweet text, r integer, f integer);
alter user postgres with PASSWORD 'mercuryminds';



insert into mmtweet values ('1','mm','2015-01-12 13:30:07
mm'# ', 'Donât shy away from #mcommerce . Try it out today itself... http://t.co/ZEQwKy6ydv http://t.co/IMTosu1KT3'
mm(# , 2, 1)