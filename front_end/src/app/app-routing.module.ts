import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {NavComponent} from "./nav/nav.component";

const routes: Routes = [];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  declarations: [
    NavComponent
  ],
  exports: [RouterModule, NavComponent]
})
export class AppRoutingModule { }
