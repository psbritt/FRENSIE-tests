//---------------------------------------------------------------------------//
//!
//! \file   h_spheres.c
//! \author Luke Kersting
//! \brief  Geometry for Electron H-1 sphere verification problem
//!
//---------------------------------------------------------------------------//

void h_spheres()
{
  // Set up manager of the geometry world
  gSystem->Load( "libGeom" );

  TGeoManager* geom = new TGeoManager(
                   "h_spheres",
                   "Geometry for the electron H-1 spheres at room temp test prob.");

  // Create the hydrogen material
  TGeoMaterial* mat_1 = new TGeoMaterial( "mat_1", 1, 1, -0.01 );
  TGeoMedium* med_1 = new TGeoMedium( "med_1", 2, mat_1 );

  // Create the void material
  TGeoMaterial* void_mat = new TGeoMaterial( "void", 0, 0, 0 );
  TGeoMedium* void_med = new TGeoMedium( "void_med", 1, void_mat );

  // Create the graveyard
  TGeoMaterial* graveyard_mat = new TGeoMaterial( "graveyard", 0, 0, 0 );
  TGeoMedium* graveyard_med = new TGeoMedium( "graveyard", 3, graveyard_mat );

  // Create the hydrogen volume 1
  TGeoVolume* h_sphere_volume1 =
    geom->MakeSphere( "SPHERE1", med_1, 0.0, 0.0005 );

  h_sphere_volume1->SetUniqueID( 1 );

  // Create the hydrogen volume 2
  TGeoVolume* h_sphere_volume2 =
    geom->MakeSphere( "SPHERE2", med_1, 0.0, 0.0010 );

  h_sphere_volume2->SetUniqueID( 2 );

  // Create the hydrogen volume 3
  TGeoVolume* h_sphere_volume3 =
    geom->MakeSphere( "SPHERE3", med_1, 0.0, 0.0015 );

  h_sphere_volume3->SetUniqueID( 3 );

  // Create the hydrogen volume 4
  TGeoVolume* h_sphere_volume4 =
    geom->MakeSphere( "SPHERE4", med_1, 0.0, 0.0020 );

  h_sphere_volume4->SetUniqueID( 4 );

  // Create the hydrogen volume 5
  TGeoVolume* h_sphere_volume5 =
    geom->MakeSphere( "SPHERE5", med_1, 0.0, 0.0025 );

  h_sphere_volume5->SetUniqueID( 5 );

  // Create the void volume
  TGeoVolume* void_sphere_volume =
    geom->MakeSphere( "VOID", void_med, 0.0, 45.0 );

  void_sphere_volume->SetUniqueID( 6 );

  // Create the graveyard volume
  TGeoVolume* graveyard_volume =
    geom->MakeSphere( "GRAVEYARD", graveyard_med, 0.0, 50.0 );

  graveyard_volume->SetUniqueID( 7 );

  // Place the hydrogen sphere 1 inside of hydrogen sphere 2
  h_sphere_volume2->AddNode( h_sphere_volume1, 1 );

  // Place the hydrogen sphere 2 inside of hydrogen sphere 3
  h_sphere_volume3->AddNode( h_sphere_volume2, 1 );

  // Place the hydrogen sphere 3 inside of hydrogen sphere 4
  h_sphere_volume4->AddNode( h_sphere_volume3, 1 );

  // Place the hydrogen sphere 4 inside of hydrogen sphere 5
  h_sphere_volume5->AddNode( h_sphere_volume4, 1 );

  // Place the hydrogen sphere 5 inside of the void sphere
  void_sphere_volume->AddNode( h_sphere_volume5, 1 );

  // Place the void sphere inside of the graveyard
  graveyard_volume->AddNode( void_sphere_volume, 1 );
  geom->SetTopVolume( graveyard_volume );

  // Close the geometry
  geom->SetTopVisible();
  geom->CloseGeometry();

  // Draw the geometry
  // h_sphere_volume5->Draw();

  // Export the geometry
  geom->Export( "h_spheres.root" );

  // Finished
  exit(0);
}

//---------------------------------------------------------------------------//
// end h_sphere.c
//---------------------------------------------------------------------------//
