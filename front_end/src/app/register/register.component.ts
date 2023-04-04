import {Component} from "@angular/core";
import {FormBuilder, Validators} from "@angular/forms";
import {WebService} from "../web.service";
import {ActivatedRoute, Router} from "@angular/router";


@Component({
  selector: 'register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})

export class RegisterComponent {
  registrationForm: any;
  public siteKey: any;

  constructor(public webService: WebService, private router: Router, private formBuilder: FormBuilder) {
  }

  ngOnInit() {

    this.registrationForm = this.formBuilder.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: ['', Validators.required],
      password: ['', Validators.required],
      postcode: ['', Validators.required],
      otp: ['', Validators.required],
      recaptcha: ['', Validators.required]
    });
    this.siteKey = "6LfJZPwjAAAAAANhjiBGN5hCBYhL4wCh4-_eFnUv"

  }

  onSubmit() {
    //console log for testing
    console.log(this.registrationForm.value);
    this.webService.addVoter(this.registrationForm.value).subscribe(
      () => { this.router.navigate(['/login']);
    },
      (error) => {
        console.error('Error sending OTP:', error);
      }
    );
  }
}
