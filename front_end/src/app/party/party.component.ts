import {Component} from "@angular/core";
import {WebService} from "../services/web.service";
import {ActivatedRoute} from "@angular/router";
import {FormBuilder} from "@angular/forms";

@Component({
  selector: 'party',
  templateUrl: './party.component.html',
  styleUrls: ['./party.component.css']
})

export class PartyComponent {

  party_list: any = [];

   constructor(public webService: WebService, private route: ActivatedRoute, private formBuilder: FormBuilder) {
  }

  ngOnInit() {
       this.webService.getParty(this.route.snapshot.params['id']).subscribe(partyData => {
    this.party_list = partyData;
  });
  }
}
