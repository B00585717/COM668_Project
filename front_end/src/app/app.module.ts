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
import {ProfileComponent} from './profile.component';
import {NgxCaptchaModule} from "ngx-captcha";
import {FormsModule} from '@angular/forms';
import {LogoutComponent} from "./logout.component";
import {VerificationComponent} from "./verification.component"


var routes: any = [
  {
    path: '',
    component: HomeComponent
  },
    {
    path: 'verification',
    component: VerificationComponent
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
  },
  {
    path: 'profile',
    component: ProfileComponent
  },
  {
    path: 'logout',
    component: LogoutComponent
  }

  ]


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    RegisterComponent,
    LoginComponent,
    CandidateComponent,
    PartyComponent,
    CandidatesComponent,
    PartiesComponent,
    ProfileComponent,
    LogoutComponent,
    VerificationComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    ReactiveFormsModule,
    NgxCaptchaModule,
    FormsModule
  ],
  providers: [WebService],
  bootstrap: [AppComponent]
})
export class AppModule { }
