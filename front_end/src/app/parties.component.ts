import {Component} from "@angular/core";
import {WebService} from "./web.service";
import {ActivatedRoute} from "@angular/router";
import {FormBuilder} from "@angular/forms";

@Component({
  selector: 'parties',
  templateUrl: './parties.component.html',
  styleUrls: ['./parties.component.css']
})

export class PartiesComponent {

  party_list: any = [];
  party: any;

  party_form: any;


  constructor(public webService: WebService, private route: ActivatedRoute, private formBuilder: FormBuilder) {
  }

  ngOnInit() {
    this.party_list = this.webService.getParties();
    this.party = this.webService.getParty(this.party_list.partyId)
  }

  onSubmit() {
    this.webService.addParty(this.party_form.value).subscribe((response: any) => {
      this.party_form.reset();
    });

    this.party_form = this.formBuilder.group({
      party_name: '',
      image: '',
      manifestio: ''
    });

    this.party_list = this.webService.getParties();
    this.party_list = this.webService.getParty(this.route.snapshot.params['id']);
  }
}
