<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta name = "viewport" content="width=device-width, initial-scale=1.0">
		<meta http-equiv="X-UA-Compatible" content="ie=edge">
		<title>ChartJS - Pie Chart</title>
		<script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.4/dist/Chart.min.js"></script>
		<link rel="stylesheet" href = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">

	</head>
	<body>
		<a href="../index.php"> Back</a>
		<div class="container">
			<canvas id="myChart"></canvas>
		</div>

<?php
  $F = fopen("../Tools/probability.txt","r");

  if($F){

      while (($probability = fgetcsv($F, 1000, " ")) !== FALSE) {

        foreach($probability as $p){

          $probabilities[] = $p;
		  
        }
	}
      fclose($F);
  	}
?>

		<script>
			let myChart = document.getElementById('myChart').getContext('2d');

			let barChart = new Chart(myChart,{

				type:'doughnut', //bar,pie

				data:{

					labels:['Covid','Normal'],

					datasets:[{
							label:'probability',

							data:[ <?php echo $probabilities[1];?> , <?php echo $probabilities[3];?> ],

							backgroundColor:['#CD0B45','#2A72B9']
						}]
				},

				options:{}

			});
			
		</script>
	</body>
</html>