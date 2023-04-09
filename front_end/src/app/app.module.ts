import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {HomeComponent} from './home/home.component';
import {RouterModule} from "@angular/router";
import {HttpClientModule} from "@angular/common/http";
import {WebService} from "./services/web.service";
import {RegisterComponent} from './register/register.component';
import {LoginComponent} from './login/login.component';
import {CandidatesComponent} from './candidates/candidates.component';
import {CandidateComponent} from './candidate/candidate.component';
import {PartiesComponent} from './parties/parties.component';
import {PartyComponent} from './party/party.component';
import {ReactiveFormsModule} from "@angular/forms";
import {ProfileComponent} from './profile/profile.component';
import {NgxCaptchaModule} from "ngx-captcha";
import {FormsModule} from '@angular/forms';
import {LogoutComponent} from "./logout/logout.component";
import {VerificationComponent} from "./register/verification.component"
import { AuthService } from './services/auth.service';
import {NavComponent} from "./nav/nav.component";
import {Password_changeComponent} from "./profile/password_change.component";
import {AdminComponent} from "./admin/admin.component";


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
  },
  {
    path: 'profile/:g_id',
    component: Password_changeComponent
  },
  {
    path: 'admin',
    component: AdminComponent
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
    VerificationComponent,
    NavComponent,
    Password_changeComponent,
    AdminComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    ReactiveFormsModule,
    NgxCaptchaModule,
    FormsModule,
    CommonModule
  ],
  providers: [WebService, AuthService],
  bootstrap: [AppComponent]
})
export class AppModule { }
