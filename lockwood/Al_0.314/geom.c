//---------------------------------------------------------------------------//
//!
//! \file   geom.c
//! \author Luke Kersting
//! \brief  1st geometry for 0.314 MeV Electron energy deposition in Al validation problem
//!
//---------------------------------------------------------------------------//

void geom()
{
  // Set up manager of the geometry world
  gSystem->Load( "libGeom" );
  TGeoManager* geom = new TGeoManager(
    "geom",
    "Geometry for 0.314 MeV Electron energy deposition in Al test prob.");

//---------------------------------------------------------------------------//
// Material and Mixture Definitions
//---------------------------------------------------------------------------//

  // Al ( density given as 2.7 not 2.69890 g/cm^3 )
  density = 2.7;
  TGeoMaterial* mat_1 = new TGeoMaterial( "mat_1", 26.9815385, 13, -density );

  // Void material
  TGeoMaterial* void_mat = new TGeoMaterial( "void", 0, 0, 0 );

  // Graveyard (terminal)
  TGeoMaterial* graveyard_mat = new TGeoMaterial( "graveyard", 0, 0, 0 );

//---------------------------------------------------------------------------//
// Medium Definitions
//---------------------------------------------------------------------------//

  // Al
  TGeoMedium* med_1 = new TGeoMedium( "med_1", 1, mat_1 );

  // Void
  TGeoMedium* void_med = new TGeoMedium( "void_med", 2, void_mat );

  // Graveyard
  TGeoMedium* graveyard_med = new TGeoMedium( "graveyard", 3, graveyard_mat );

//---------------------------------------------------------------------------//
// Volume Definitions
//---------------------------------------------------------------------------//

  //----------------------------
  // Create the calorimeter foil
  //----------------------------

  // Thickness of the calorimeter foil (given in g/cm^2)
  double calorimeter_thickness = 5.050E-03/density;
  // Half the height
  double half_cal_thickness = calorimeter_thickness/2.0;

  // Height (given - largest dimension)
  double height = 8.255;
  // Half side length
  double half_height = height/2.0;

  TGeoVolume* calorimeter_foil =
    geom->MakeBox( "Calorimeter_Foil", med_1, half_height, half_height, half_cal_thickness );

  calorimeter_foil->SetUniqueID( 1 );
  calorimeter_foil->SetLineColor( 2 );

  // //----------------------
  // // Create the front foil
  // //----------------------

  // Range of dose depth calculation in cm ( 0.0009, 0.0035, 0.0067, 0.0095,
  // 0.0124, 0.0149, 0.0177, 0.021, 0.0242, 0.0267, 0.03, or 0.0368 )
  double range = 0.0368;

  // Calculate the thickness of the front foil
  double front_thickness = range - half_cal_thickness;

  TGeoVolume* front_foil;
  if (front_thickness > 0.0 )
  {
    // Height (given - largest dimension)
    height = 8.89;
    // Half side length
    half_height = height/2.0;

    front_foil =
      geom->MakeBox( "Front_Foil", med_1, half_height, half_height, front_thickness/2.0 );

    front_foil->SetUniqueID( 2 );
    front_foil->SetLineColor( 3 );
  }

  //--------------------------------------------------------
  // Create the infinite plate (D = 7.62 cm, h = "infinite")
  //--------------------------------------------------------

  double plate_radius = 3.81;
  double plate_half_length = 0.5;
  TGeoVolume* infinite_plate =
    geom->MakeTube( "Infinite_Plate", med_1, 0.0, plate_radius, plate_half_length );

  infinite_plate->SetUniqueID( 3 );
  infinite_plate->SetLineColor( 4 );

  //--------------------------------------------------------
  // Create the vacuum (R = "infinite" cm, h = "infinite")
  //--------------------------------------------------------

  // Set a radius of 7 cm ( 167 x the CSDA range )
  double vacuum_radius = 7.0;
  // Set a vacuum length large enough to cover the whole geometry
  double vacuum_half_length = 2.0*plate_half_length + 5.0 + calorimeter_thickness + 0.5;
  // Add region
  TGeoVolume* void_region =
    geom->MakeTube( "Void", void_med, 0.0, vacuum_radius, vacuum_half_length );

  void_region->SetUniqueID( 4 );
  void_region->SetLineColor( 6 );
  void_region->SetVisibility( true );

  //--------------------------------------------------------
  // Create the graveyard (encompasses the entire geometry)
  //--------------------------------------------------------

  // Add region
  TGeoVolume* graveyard_region =
    geom->MakeTube( "Graveyard", graveyard_med, 0.0, vacuum_radius + 0.5, vacuum_half_length + 0.5 );

  graveyard_region->SetUniqueID( 5 );
  graveyard_region->SetLineColor( 7 );
  graveyard_region->SetVisContainers( true );

//---------------------------------------------------------------------------//
// Heirarchy (Volume) Definitions
//---------------------------------------------------------------------------//

// Set graveyard as the top volume
geom->SetTopVolume(graveyard_region);

  //------------------------
  // Add vacuum to graveyard
  //------------------------
  // Get z position of the vacuum
  double vacuum_z = vacuum_half_length;
  // Add region
  graveyard_region->AddNode(void_region, 1 );

    //-----------------------------------
    // Add the calorimeter foil to vacuum
    //-----------------------------------

    // Set the front of the calorimeter at a z of 5 cm
    double calorimeter_z = 5.0 + half_cal_thickness;
    // Add the front calorimeter foil to vacuum
    void_region->AddNode( calorimeter_foil, 2, new TGeoTranslation(0,0,calorimeter_z) );

    //-----------------------------------
    // Add the front foil to vacuum
    //-----------------------------------

    if( front_thickness > 0.0 )
    {
      // Set the front foil 0.1 cm in front of the calorimeter
      double front_z = 4.9 - front_thickness/2.0;
      // Add the region
      void_region->AddNode( front_foil, 1, new TGeoTranslation(0,0,front_z) );
    }

    //-----------------------------------
    // Add the infinite plate to vacuum
    //-----------------------------------

    // Set the infinite plate 0.1 cm behind the  calorimeter
    double plate_z = 5.1 + calorimeter_thickness + plate_half_length;
    // Add region
    void_region->AddNode( infinite_plate, 3, new TGeoTranslation(0,0,plate_z) );


//---------------------------------------------------------------------------//
// Export and Drawing Capabilities
//---------------------------------------------------------------------------//

  // // Close the geometry
  // geom->SetTopVisible();
  // geom->CloseGeometry();

  // // Draw the geometry
  // graveyard_region->Draw();

  //  TView *view = gPad->GetView();
  //  view->ShowAxis();

  // Export the geometry
  geom->Export( "geom.root" );

  // Finished
  exit(0);
}

//---------------------------------------------------------------------------//
// end geom.c
//---------------------------------------------------------------------------//
