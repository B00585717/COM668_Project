import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {HomeComponent} from './home.component';
import {RouterModule} from "@angular/router";
import {HttpClientModule} from "@angular/common/http";
import {WebService} from "./web.service";
import {RegisterComponent} from './register.component';
import {LoginComponent} from './login.component';
import {CandidatesComponent} from './candidates.component';
import {CandidateComponent} from './candidate.component';
import {PartiesComponent} from './parties.component';
import {PartyComponent} from './party.component';
import {ReactiveFormsModule} from "@angular/forms";
import {NgxCaptchaModule} from "ngx-captcha";


var routes: any = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'register',
    component: RegisterComponent
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'parties',
    component: PartiesComponent
  },
  {
    path: 'parties/:id',
    component: PartyComponent
  },
  {
    path: 'candidates',
    component: CandidatesComponent
  },
  {
    path: 'candidates/:id',
    component: CandidateComponent
  }

  ]


@NgModule({
  declarations: [
    AppComponent, HomeComponent, RegisterComponent, LoginComponent, CandidateComponent, PartyComponent, CandidatesComponent, PartiesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    ReactiveFormsModule,
    NgxCaptchaModule
  ],
  providers: [WebService],
  bootstrap: [AppComponent]
})
export class AppModule { }
