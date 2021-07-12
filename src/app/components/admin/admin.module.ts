import {NgModule} from "@angular/core";
import {Routes, RouterModule} from "@angular/router";
import {AdminComponent} from "./admin/admin.component";
import {CommonModule} from "@angular/common";
import {SidebarComponent} from './common/sidebar/sidebar.component';
import {NavComponent} from './common/nav/nav.component';
import {ParcelsComponent} from './parcels/parcels.component';
import {TellersComponent} from './tellers/tellers/tellers.component';
import { LoginComponent } from './login/login.component';
import {ReactiveFormsModule} from "@angular/forms";
import { ParcelDetailComponent } from './parcel-detail/parcel-detail.component';
import {AuthGuard} from "../../guards/authguard.guard";

const adminRoutes: Routes = [
  {path: 'login', component: LoginComponent},
  {path: '', component: AdminComponent, canActivate: [AuthGuard]},
  {path: 'tellers', component: TellersComponent, canActivate: [AuthGuard]},
  {path: 'parcels', component: ParcelsComponent, canActivate: [AuthGuard]},
  {path: 'parcels/:slug', component: ParcelDetailComponent, canActivate: [AuthGuard]},
]

@NgModule({
  imports: [CommonModule, ReactiveFormsModule, RouterModule.forChild(adminRoutes)],
  declarations: [AdminComponent, SidebarComponent, NavComponent, ParcelsComponent, TellersComponent, LoginComponent, ParcelDetailComponent]
})
export class AdminModule {
}
