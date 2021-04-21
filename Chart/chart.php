<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clasificarea</title>
    <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/bootstrap.min.css">
    <link rel="stylesheet" href="../css/slick.css" type="text/css" /> 
    <link rel="stylesheet" href="../css/templatemo-style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.4/dist/Chart.min.js"></script>
		<link rel="stylesheet" href = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">

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
</head>

<body>

  <div class="page-container" 
  style="background-image: url('../css/med4.jpg');
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: 100% 100%;">
      <div class="container-fluid">
        <div class="row">
          <div class="col-xs-12">
            <div class="cd-slider-nav">
              <nav class="navbar navbar-expand-lg" id="tm-nav">
                <a class="navbar-brand" href="#"><h2 style="color:white;">Covid-19 Detection</h2></a>
                  <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-supported-content" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                  </button>
                  <div class="collapse navbar-collapse" id="navbar-supported-content">
                    <ul class="navbar-nav mb-2 mb-lg-0">
                      <li class="nav-item selected">
                        <a class="nav-link" aria-current="page" href="#0" data-no="1">Imaginea</a>
                        <div class="circle"></div>
                      </li>
                      <li class="nav-item">
                        <a class="nav-link" href="#0" data-no="4">Clasificare</a>
                        <div class="circle"></div>
                      </li>
                      <li class="nav-item">
                        <a class="nav-link" href="../index.php" data-no="3">Inapoi</a>
                        <div class="circle"></div>
                      </li>
                    </ul>
                  </div>
              </nav>
            </div>
          </div>          
        </div>        
      </div>      
      <div class="container-fluid tm-content-container">
        <ul class="cd-hero-slider mb-0 py-5">
          <li class="px-3" data-page-no="1">
            <div class="page-width-1 page-left">
              <div class="d-flex position-relative tm-border-top tm-border-bottom intro-container">
                <div class="intro-left tm-bg-dark">
                  <p class="mb-4" style="color:white; padding-top:10px;">
                  Detectarea timpurie a COVID-19 poate ajuta la elaborarea unui plan de tratament adecvat 
                  si a deciziilor de izolare a bolii. Astfel, in acest studiu demonstrez cum pot fi adoptate 
                  modele de retele profunde pre-antrenate pentru a efectua detectarea COVID-19 folosind 
                  imagini cu raze X. Scopul este de a oferi profesionistilor din domeniul medical suprasolcii- tati 
                  o a doua pereche de ochi prin modele inteligente de cl- asificare a imaginilor.</p>
                 
                </div>
                <div class="intro-right" style="width: 1000px;">
                  <div class="mx-auto tm-border-top gallery-slider">
                    <figure class="effect-julia item">
                      <?php 
                        $dirname = "../Image";
                        $images = scandir($dirname);
                        $ignore = Array(".", "..");
                        foreach($images as $curimg){
                            if(!in_array($curimg, $ignore)) {
                                echo "<img src='../Image/$curimg' / style='width=800px';>\n";
                            }
                        }
                      ?>
                        <figcaption>
                            <div>
                                <p>
                                  <?php if($probabilities[1]>$probabilities[3]){
                                    echo "Covid";
                                  } else{
                                    echo "Normal";
                                  }
                                  ?>
                                  </p>
                            </div>
                        </figcaption>
                    </figure>
                    </div>
                </div>
                <div class="circle intro-circle-1"></div>
                <div class="circle intro-circle-2"></div>
                <div class="circle intro-circle-3"></div>
                <div class="circle intro-circle-4"></div>
              </div>
       
            </div>            
          </li>

          <li class="px-3" data-page-no="4">
            <div class="page-width-1 page-left">
              <div class="d-flex position-relative tm-border-top tm-border-bottom intro-container">
              <div class="intro-left1" style="margin-right: 0px;
                                              padding: 0px;
                                              width: 500px;  ">
                  <div class="container">
			              <canvas id="myChart" style="color:red;"></canvas>
		              </div>
                      <script>
                          let myChart = document.getElementById('myChart').getContext('2d');
                          let barChart = new Chart(myChart,{

                            type:'doughnut', //bar,pie , doughnut

                            data:{

                              labels:['Covid','Normal'],

                              datasets:[{
                                  label:'probability',

                                  data:[ <?php echo $probabilities[1];?> , <?php echo $probabilities[3];?> ],

                                  backgroundColor:['#CD0B45','#2A72B9']
                                  
                                }]
                            },
                            
                            options: { 
                              legend: {
                                  labels: {
                                      fontColor: "white",
                                      fontSize: 18
                                  }
                              },

                            }

                          });
                      </script>
                </div>
                <div class="intro-right tm-bg-dark" style="color:white; padding-left:15px;padding-top:15px;">
                <p>
                  Rezultatul cercetarii returneaza ur- matoarea distributie probabilista:
                  <br>  Covid19 - <?php echo $probabilities[1]; echo "<br>";?> 
                   Normal - <?php echo $probabilities[3];echo "<br>";?>
                   Asadar, conform calsificarii realizate de reteaua neuronala, rezultatul spune ca pacientul  
                   <?php 
                   if($probabilities[1]>$probabilities[3]){
                        echo "este infectat cu Covid19.";
                      } else{
                        echo "este Sanatos!";
                      }
                    ?>
                </p>
                </div>
                <div class="circle intro-circle-1"></div>
                <div class="circle intro-circle-2"></div>
                <div class="circle intro-circle-3"></div>
                <div class="circle intro-circle-4"></div>
              </div>
       
            </div>            
          </li>
        </ul>
    </div>
    <div class="container-fluid">
      <footer class="row mx-auto tm-footer">
      </footer>
    </div>
  </div>
  <div id="loader-wrapper">            
    <div id="loader"></div>
    <div class="loader-section section-left"></div>
    <div class="loader-section section-right"></div>
  </div>  
  <script src="js/jquery-3.5.1.min.js"></script>
  <script src="js/bootstrap.min.js"></script>
  <script src="js/slick.js"></script>
  <script src="js/templatemo-script.js"></script>
</body>
</html>