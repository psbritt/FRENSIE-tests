//---------------------------------------------------------------------------//
//!
//! \file   problem_1.c
//! \author Luke Kersting
//! \brief  Geometry for problem_1 VR reduction (source and detector in hydrogen)
//!
//---------------------------------------------------------------------------//

void problem_1()
{
  // Set up manager of the geometry world
  gSystem->Load( "libGeom" );

  TGeoManager* geom = new TGeoManager(
                   "problem_1",
                   "Geometry for simple VR test problem");

  // Create the hydrogen gas material
  TGeoMaterial* mat_1 = new TGeoMaterial( "mat_1", 1, 1, -50.00 );
  TGeoMedium* med_1 = new TGeoMedium( "med_1", 1, mat_1 );
  
  // Create the source material (Pottasium-40)
  TGeoMaterial* mat_2 = new TGeoMaterial( "mat_2", 19, 40, -0.862 );
  TGeoMedium* med_2 = new TGeoMedium( "med_2", 2, mat_2 );
  
  // Create the detector material (Germanium-72)
  TGeoMaterial* mat_3 = new TGeoMaterial( "mat_3", 32, 72, -5.323 );
  TGeoMedium* med_3 = new TGeoMedium( "med_3", 3, mat_3 );
  
  // Create the graveyard
  TGeoMaterial* graveyard_mat = new TGeoMaterial( "graveyard", 0, 0, 0 );
  TGeoMedium* graveyard_med = new TGeoMedium( "graveyard", 4, graveyard_mat );

  // Create the hydrogen volume containing source and detector
  TGeoVolume* hydrogen_volume =
    geom->MakeBox( "HYDROGEN", med_1, 1000.0 , 600.0 , 500.0 );
    
   hydrogen_volume->SetUniqueID( 1 );
    
  // Create the source volume
  TGeoVolume* source_volume =
    geom->MakeBox( "SOURCE", med_2, 40.0, 40.0, 40.0 );

  source_volume->SetUniqueID( 2 );

  // Create the detector volume
  TGeoVolume* detector_volume =
    geom->MakeBox( "DETECTOR", med_3, 40.0, 40.0, 40.0 );

  detector_volume->SetUniqueID( 3 );

  // Create the graveyard volume
  TGeoVolume* graveyard_volume =
    geom->MakeBox( "TERMINAL", graveyard_med, 1001.0, 501.0, 501.0 );

  graveyard_volume->SetUniqueID( 4 );
   
  // Set the "container" volume
  geom->SetTopVolume( graveyard_volume );

  // Position the source
  TGeoTranslation *source_tr = new TGeoTranslation( -900.0, 0.0, 0.0);
  
  // Position the detector
  TGeoTranslation *detector_tr = new TGeoTranslation( 900.0, 0.0, 0.0);

  // Place the hydrogen inside the graveyard
  
  graveyard_volume->AddNode( hydrogen_volume, 1 );
  
  // Place the source and detector inside the hydrogen volume using above translations
  
  hydrogen_volume->AddNode( source_volume, 1, source_tr );
  hydrogen_volume->AddNode( detector_volume, 1, detector_tr);

  // Close the geometry
  geom->SetTopVisible();
  geom->CloseGeometry();

  // Draw the geometry
  //graveyard_volume->Draw();

  // Export the geometry
  geom->Export( "problem_1.root" );

  // Finished
  exit(0);
}

//---------------------------------------------------------------------------//
// end problem_1.c
//---------------------------------------------------------------------------//
