import {Component} from "@angular/core";
import {FormBuilder, Validators} from "@angular/forms";
import {WebService} from "../services/web.service";
import {Router} from "@angular/router";
import { HttpClient } from '@angular/common/http';
import { EmailService } from '../services/email.service';


@Component({
  selector: 'register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})

export class RegisterComponent {
  registrationForm: any;
  public siteKey: any;
  email: any;
  postcode_regex = '^([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([AZa-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z])))) [0-9][A-Za-z]{2})$'

  constructor(public webService: WebService,
              private router: Router,
              private formBuilder: FormBuilder,
              private http: HttpClient,
              private emailService: EmailService) {
  }

  ngOnInit() {
    const navigation = this.router.getCurrentNavigation();
    const emailFromVerification = navigation && navigation.extras.state && navigation.extras.state["email"];

    this.registrationForm = this.formBuilder.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: [emailFromVerification || '', Validators.required],
      password: ['', Validators.required],
      postcode: ['', Validators.pattern(this.postcode_regex)],
      otp: ['', Validators.required],
      recaptcha: ['', Validators.required]
    });
    this.siteKey = "6LfJZPwjAAAAAANhjiBGN5hCBYhL4wCh4-_eFnUv"

    this.emailService.currentEmail.subscribe((email) => {
      this.registrationForm.controls['email'].setValue(email);
    });
  }

  onSubmit() {
    //console log for testing
    console.log("Data being sent:", this.registrationForm.value);
    this.webService.addVoter(this.registrationForm.value).subscribe(
      (response) => {
        console.log("Success:", response); // Add this line to log the successful response
      this.router.navigate(['/login']);
    },
      (error) => {
        console.error('onSubmitError:', error);
      }
    );
  }
}
