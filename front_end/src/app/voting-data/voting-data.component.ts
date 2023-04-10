// voting-data.component.ts
import { Component, OnInit } from '@angular/core';
import { WebService } from '../services/web.service';

@Component({
  selector: 'app-voting-data',
  templateUrl: './voting-data.component.html'
})
export class VotingDataComponent implements OnInit {
  votingData: any[] = [];

  constructor(private webService: WebService) { }

  ngOnInit(): void {
    this.webService.getVotingData().subscribe((data: any) => {
      this.votingData = data;
    });
  }

}
