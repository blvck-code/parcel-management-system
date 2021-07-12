import {NgModule} from "@angular/core";
import {CommonModule} from "@angular/common";
import {Routes, RouterModule} from "@angular/router";

import {ParcelsComponent} from "./parcels/parcels.component";
import {ParcelAddComponent} from './parcel-add/parcel-add.component';
import {NavComponent} from './common/nav/nav.component';
import {ParcelDetailComponent} from './parcel-detail/parcel-detail.component';
import {ParcelsResolverService} from "../../resolvers/parcels-resolver.service";
import {ReactiveFormsModule} from "@angular/forms";

const parcelRoutes: Routes = [
  {path: '', component: ParcelsComponent},
  {path: 'add', component: ParcelAddComponent, resolve: {parcels: ParcelsResolverService}},
  {path: ':slug', component: ParcelDetailComponent, resolve: {parcels: ParcelsResolverService}},
]

@NgModule({
  imports: [CommonModule, ReactiveFormsModule, RouterModule.forChild(parcelRoutes)],
  declarations: [ParcelsComponent, ParcelAddComponent, NavComponent, ParcelDetailComponent]
})
export class ParcelsModule {
}
