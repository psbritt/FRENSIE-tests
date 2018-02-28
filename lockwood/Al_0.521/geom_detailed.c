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

  // Define some rotations (90, 180, 270 degrees about the z-axis)
  TGeoRotation *rot1 = new TGeoRotation("rot1", 90, 0, 0);
  rot1->RegisterYourself();
  TGeoRotation *rot2 = new TGeoRotation("rot2", 180, 0, 0);
  rot2->RegisterYourself();
  TGeoRotation *rot3 = new TGeoRotation("rot3", 270, 0, 0);
  rot3->RegisterYourself();

  //-----------------------------
  // Create the calorimeter foils (make into two halves)
  //-----------------------------

  // Thickness of the calorimeter foil (given)
  double calorimeter_thickness = 5.050E-03/density;
  double quarter_thickness = calorimeter_thickness/4.0;
  // Height (given - largest dimension)
  double height = 8.255;
  // Length of side 1 (given)
  double length_1 = 3.175;

  // Calculate length of side 2
  double length_2 = (height - length_1)/sqrt(2.0);
  // Calculate radius of wedge 1 (distance from center to middle edge of side 1)
  double radius_1 = height/2.0;
  // Calculate radius of wedge 2 (distance from center to middle edge of side 2)
  double radius_2 = ( height + length_1 )/(sqrt(8.0));

  // // Calculate the inner angle of wedge 1
  // double theta_1 = 2.0*atan(length_1/height)*180.0/M_PI;
  // // Calculate the angle off the x-axis of wedge 1
  // double phi_1 = 90.0 - 0.5*theta_1;

  // // Calculate the inner angle of wedge 2
  // double theta_2 = 2.0*atan(length_2/(2.0*radius_2))*180.0/M_PI;
  // // Calculate the angle off the x-axis of wedge 1
  // double phi_2 = 90.0 + theta_1/2.0;

  // Set the calorimeter at a z of 5 cm
  // Calorimeter lower z-position
  double calorimeter_lower_z = 5.0;
  // Calorimeter upper z-position
  double calorimeter_upper_z = calorimeter_lower_z + calorimeter_thickness;

  // // Create wedge 1
  // TGeoPgon* wedge1 = new TGeoPgon("wedge1", phi_1, theta_1, 1, 2);
  // wedge1->DefineSection(0, calorimeter_lower_z, 0, radius_1);
  // wedge1->DefineSection(1, calorimeter_upper_z, 0, radius_1);

  // // Create wedge 2
  // TGeoPgon* wedge2 = new TGeoPgon("wedge2", phi_2, theta_2, 1, 2);
  // wedge2->DefineSection(0, calorimeter_lower_z, 0, radius_2);
  // wedge2->DefineSection(1, calorimeter_upper_z, 0, radius_2);

  // // Create composite of wedge 1 and wedge 2
  // TGeoCompositeShape* comp_wedge1 = new TGeoCompositeShape("comp_wedge1","wedge1+wedge2");

  // // Translate wedge half the thickness of the calorimeter
  // TGeoTranslation *tran1 =
  //   new TGeoTranslation("tran1", 0, 0, calorimeter_thickness/2.0);
  // tran1->RegisterYourself();

  // // Create pentagon by combining 4 composite wedges rotated about the z-axis
  // TGeoCompositeShape* foil1 = new TGeoCompositeShape("foil1",
  // "comp_wedge1+comp_wedge1:rot1+comp_wedge1:rot2+comp_wedge1:rot3");

  // TGeoVolume* calorimeter_foil = new TGeoVolume( "Calorimeter_Foil", foil1, med_1 );

  TGeoBBox* half_calorimeter_foil = new TGeoBBox("half_foil", radius_1, radius_1, quarter_thickness);

  TGeoVolume* front_calorimeter_foil =
    new TGeoVolume( "Front_Calorimeter_Foil", half_calorimeter_foil, med_1 );

  front_calorimeter_foil->SetUniqueID( 1 );
  front_calorimeter_foil->SetLineColor( 2 );

  TGeoVolume* back_calorimeter_foil =
    new TGeoVolume( "Back_Calorimeter_Foil", half_calorimeter_foil, med_1 );

  back_calorimeter_foil->SetUniqueID( 2 );
  back_calorimeter_foil->SetLineColor( 9 );

  //----------------------
  // Create the front foil
  //----------------------

  // // Thickness of the front foil (given)
  // double range = 0.0035; // Range of dose depth calculation in cm
  // double front_thickness = range - calorimeter_thickness/2.0;
  // // Height (given - largest dimension)
  // height = 8.89;
  // // Length of side 1 (given)
  // length_1 = 6.03;

  // // Calculate length of side 2
  // length_2 = (height - length_1)/sqrt(2.0);
  // // Calculate radius of wedge 3 (distance from center to middle edge of side 1)
  // radius_1 = height/2.0;
  // // Calculate radius of wedge 4 (distance from center to middle edge of side 2)
  // radius_2 = ( height + length_1 )/(sqrt(8.0));

  // // // Calculate the inner angle of wedge 1
  // // theta_1 = 2.0*atan(length_1/height)*180.0/M_PI;
  // // // Calculate the angle off the x-axis of wedge 1
  // // phi_1 = 90.0 - 0.5*theta_1;

  // // // Calculate the inner angle of wedge 2
  // // theta_2 = 2.0*atan(length_2/(2.0*radius_2))*180.0/M_PI;
  // // // Calculate the angle off the x-axis of wedge 1
  // // phi_2 = 90.0 + theta_1/2.0;

  // // Set the front foil 0.1 in front of the calorimeter foil
  // // Front foil upper z-position
  // double front_upper_z = calorimeter_lower_z - 0.1;
  // // Front foil lower z-position
  // double front_lower_z = front_upper_z - front_thickness;

  // // // Create wedge 3
  // // TGeoPgon* wedge3 = new TGeoPgon("wedge3", phi_1, theta_1, 1, 2);
  // // wedge3->DefineSection(0, front_lower_z, 0, radius_1);
  // // wedge3->DefineSection(1, front_upper_z, 0, radius_1);

  // // // Create wedge 2
  // // TGeoPgon* wedge4 = new TGeoPgon("wedge4", phi_2, theta_2, 1, 2);
  // // wedge4->DefineSection(0, front_lower_z, 0, radius_2);
  // // wedge4->DefineSection(1, front_upper_z, 0, radius_2);

  // // // Create composite of wedge 1 and wedge 2
  // // TGeoCompositeShape* comp_wedge2 = new TGeoCompositeShape("comp_wedge2","wedge3+wedge4");

  // // // Create pentagon by combining 4 composite wedges rotated about the z-axis
  // // TGeoCompositeShape* foil2 = new TGeoCompositeShape("foil2",
  // // "comp_wedge2+comp_wedge2:rot1+comp_wedge2:rot2+comp_wedge2:rot3");

  // // TGeoVolume* front_foil = new TGeoVolume( "Front_Foil", foil2, med_1 );

  // TGeoVolume* front_foil =
  //   geom->MakeBox( "Front_Foil", med_1, radius_1, radius_1, front_thickness/2.0 );

  // front_foil->SetUniqueID( 3 );
  // front_foil->SetLineColor( 3 );

  //--------------------------------------------------------
  // Create the infinite plate (D = 7.62 cm, h = "infinite")
  //--------------------------------------------------------

  double plate_radius = 3.81;
  double plate_half_length = 0.5;
  TGeoVolume* infinite_plate =
    geom->MakeTube( "Infinite_Plate", med_1, 0.0, plate_radius, plate_half_length );

  infinite_plate->SetUniqueID( 4 );
  infinite_plate->SetLineColor( 4 );

  // Create the void region (R = 61 cm, h = 50 cm)
  // The radius is unimportant and is made smaller
  double vacuum_radius = 7.0;
  double vacuum_half_length = 2.0*plate_half_length + calorimeter_upper_z + 0.5;
  TGeoVolume* void_region =
    geom->MakeTube( "Void", void_med, 0.0, vacuum_radius, vacuum_half_length );

  void_region->SetUniqueID( 5 );
  void_region->SetLineColor( 6 );
  void_region->SetVisibility( true );

  // Create the graveyard region (R = 62 cm, h = 51 cm)
  double radius = vacuum_radius + 1.0;
  double half_length = vacuum_half_length + 0.5;
  TGeoTube *graveyard_shape = new TGeoTube("graveyard_shape", 0, radius, half_length);

  TGeoVolume* graveyard_region =
    new TGeoVolume( "Graveyard", graveyard_shape, graveyard_med );

  graveyard_region->SetUniqueID( 6 );
  graveyard_region->SetLineColor( 7 );
  // graveyard_region->SetVisibility( true );

//---------------------------------------------------------------------------//
// Heirarchy (Volume) Definitions
//---------------------------------------------------------------------------//

// geom->SetTopVolume(graveyard_region);

//   // Get z position of the vacuum
//   double vacuum_z = vacuum_half_length;
//   // Add vacuum to graveyard
//   graveyard_region->AddNode(void_region, 1 );
//   graveyard_region->SetVisContainers( true );

//     // Add the front foil to vacuum
//     // void_region->AddNode( front_foil, 1 );
//     double front_z = front_lower_z + front_thickness/2.0;
//     void_region->AddNode( front_foil, 1, new TGeoTranslation(0,0,front_z) );

//     // Add the calorimeter foil to vacuum
//     // void_region->AddNode( calorimeter_foil, 2 );
//     double calorimeter_z = calorimeter_lower_z + calorimeter_thickness/2.0;
//     void_region->AddNode( calorimeter_foil, 2, new TGeoTranslation(0,0,calorimeter_z) );

  printf("\nfront_lower_z = %e\n", front_lower_z );
  printf("\nfront_upper_z = %e\n", front_upper_z );
  printf("\nfront_thickness/2.0 = %e\n", front_thickness/2.0 );
  printf("\nfront_thickness + front_lower_z = %e\n", front_thickness + front_lower_z);
  printf("\ncalorimeter_lower_z = %e\n", calorimeter_lower_z );


//     // Get z position of the infinite plate
//     double plate_z = plate_half_length + calorimeter_upper_z + 0.1;
//     // Add the infinite plate to vacuum
//     void_region->AddNode( infinite_plate, 3, new TGeoTranslation(0,0,plate_z) );


    // Add the front foil to vacuum
    double front_z = front_lower_z + front_thickness/2.0;
    void_region->AddNode( front_foil, 1, new TGeoTranslation(0,0,front_z) );

    // Add the front calorimeter foil to vacuum
    double calorimeter_z = calorimeter_lower_z + quarter_thickness;
    void_region->AddNode( front_calorimeter_foil, 2, new TGeoTranslation(0,0,calorimeter_z) );

    // Add the back calorimeter foil to vacuum
    calorimeter_z += calorimeter_thickness/2.0;
    void_region->AddNode( back_calorimeter_foil, 2, new TGeoTranslation(0,0,calorimeter_z) );

    // Get z position of the infinite plate
    double plate_z = plate_half_length + calorimeter_upper_z + 0.1;
    // Add the infinite plate to vacuum
    void_region->AddNode( infinite_plate, 3, new TGeoTranslation(0,0,plate_z) );

  // Get z position of the vacuum
  double vacuum_z = vacuum_half_length;
  // Add vacuum to graveyard
  graveyard_region->AddNode(void_region, 1 );
  graveyard_region->SetVisContainers( true );

geom->SetTopVolume(graveyard_region);



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
// end h_sphere_1kev.c
//---------------------------------------------------------------------------//
